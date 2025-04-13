import os
import json
import traceback
import subprocess
import tempfile
from typing import Any

import dspy
from utils.llm_config import DataPreprocesserSignature


class DataPreprocesser:
    def __init__(self):
        self.module = dspy.ChainOfThought(DataPreprocesserSignature)

    def get_code_template(self) -> str:
        """
        Returns a unified code template that includes both the execution environment
        and a clearly marked section for the LLM to generate code.

        Returns:
            Unified code template as a string
        """
        return """
import pandas as pd
import numpy as np
import json
import traceback

try:
    # Load the data with specified sheet
    df = pd.read_excel('{data_path}', sheet_name='{sheet_name}')
    
    # ------ BEGIN GENERATED CODE ------
    # Convert date columns if needed - be careful with datetime operations
    # If you need to work with dates, first check the column type and convert if needed
    # Example: if 'year' column contains date strings like '2005-01-01'
    # df['year'] = pd.to_datetime(df['year']) if not pd.api.types.is_datetime64_any_dtype(df['year']) else df['year']
{generated_code}
    # ------ END GENERATED CODE ------
    
    # Return the result as JSON
    result_json = processed_df.to_json(orient='records')
    print(result_json)
except Exception as e:
    error_msg = {{'error': f'Code execution error: {{str(e)}}', 'traceback': traceback.format_exc()}}
    print(json.dumps(error_msg))
"""

    def generate_code(
        self,
        preprocessing_instructions: str,
        data_description: str,
        data_sample: str,
        data_path: str = None,
        sheet_name: str = None,
        code_template: str = None,
        chart_id: str = None,
        target_channels: list[dict[str, str]] = None,
        previous_code: str = None,
        previous_error: str = None,
    ) -> str:
        """
        Generate pandas code based on preprocessing instructions to be inserted into template

        Args:
            preprocessing_instructions: Instructions for data processing
            data_description: Description of the dataset
            data_sample: Sample of the dataset
            data_path: Path to the data file
            sheet_name: Name of the Excel sheet to use
            code_template: Optional template where generated code will be inserted

        Returns:
            Complete code with generated parts inserted into template
        """
        # Use default template if none provided
        if code_template is None:
            code_template = self.get_code_template()

        try:
            response = self.module(
                preprocessing_instructions=preprocessing_instructions,
                data_description=data_description,
                data_sample=data_sample,
                code_template=code_template,
                chart_id=chart_id,
                target_channels=target_channels,
                previous_code=previous_code,
                previous_error=previous_error,
            )

            # if start with ```
            if response.pandas_code.startswith("```python\n"):
                response.pandas_code = response.pandas_code[11:]
            if response.pandas_code.endswith("\n```"):
                response.pandas_code = response.pandas_code[:-3]

            # Insert the generated code into the template
            complete_code = code_template.format(
                generated_code=response.pandas_code,
                data_path=data_path,
                sheet_name=(
                    sheet_name if sheet_name else "0"
                ),  # Default to first sheet if not specified
            )
            # Return both the code and the channel mapping
            return {
                "code": complete_code,
                "channel_mapping": response.channel_mapping
            }
        except Exception as e:
            traceback.print_exc()
            return f"Error generating preprocessing code: {str(e)}"

    def process_with_retry(
        self,
        preprocessing_instructions: str,
        data_description: str,
        data_sample: str,
        data_path: str,
        sheet_name: str = None,
        code_template: str = None,
        chart_id: str = None,
        target_channels: list[dict[str, str]] = None,
        max_attempts: int = 3,
    ) -> Any:
        """
        Generate and execute code with automatic retry on failure.

        Args:
            preprocessing_instructions: Instructions for data processing
            data_description: Description of the dataset
            data_sample: Sample of the dataset
            data_path: Path to the data file
            sheet_name: Name of the Excel sheet to use
            code_template: Optional template where generated code will be inserted
            chart_id: ID of the chart to use
            target_channels: Target channels for visualization
            max_attempts: Maximum number of retry attempts before giving up

        Returns:
            The processed data or error information
        """
        previous_code = None
        previous_error = None

        for attempt in range(max_attempts):
            # Generate code (with error feedback if available)
            code_result = self.generate_code(
                preprocessing_instructions=preprocessing_instructions,
                data_description=data_description,
                data_sample=data_sample,
                data_path=data_path,
                sheet_name=sheet_name,
                code_template=code_template,
                chart_id=chart_id,
                target_channels=target_channels,
                previous_code=previous_code,
                previous_error=previous_error,
            )
            
            complete_code = code_result["code"]
            channel_mapping = code_result["channel_mapping"]

            # Execute the generated code
            result = self.execute_code(complete_code)

            # Check if execution was successful
            if isinstance(result, list):
                print(f"Code executed successfully on attempt {attempt + 1}")
                print(complete_code)
                # Add the channel mapping to the result
                return {
                    "data": result,
                    "channel_mapping": channel_mapping
                }

            # If we have an error and still have attempts left
            print(f"Attempt {attempt + 1} failed with error: {result['error']}")
            previous_code = complete_code
            previous_error = result.get("error", "") + "\n" + result.get("traceback", "")

            # If we've reached max attempts, return the last error
            if attempt == max_attempts - 1:
                return {
                    "error": result.get("error", ""),
                    "traceback": result.get("traceback", "")
                }

        # This should not be reached due to the return in the loop
        return {"error": "Max retry attempts reached"}

    def execute_code(self, code: str) -> Any:
        """
        Execute the generated pandas code in a separate process

        Args:
            code: The complete pandas code (with template) to execute

        Returns:
            The result of executing the code
        """
        try:
            # Format the template with the actual data path
            full_script = code

            # Create a temporary Python script with the generated code
            with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as temp_file:
                temp_file.write(full_script)
                temp_file_path = temp_file.name

            # Run the script in a separate process
            result = subprocess.run(
                ["python", temp_file_path], capture_output=True, text=True, check=True
            )

            # Clean up the temporary file
            os.unlink(temp_file_path)

            # Parse the output JSON if available
            if result.stdout:
                return json.loads(result.stdout.strip())
            else:
                return {"error": "No output from data processing script"}

        except subprocess.CalledProcessError as e:
            return {"error": f"Error executing code: {e.stderr}"}
        except Exception as e:
            traceback.print_exc()
            return {"error": f"Error in code execution: {str(e)}"}
