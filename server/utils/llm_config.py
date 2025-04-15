import os
import json
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv
import dspy

# Load environment variables
load_dotenv()

# Configure DSPy with OpenAI
def configure_dspy():
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    # Configure model with optional base URL if specified
    if api_base:
        lm = dspy.LM(model, api_key=api_key, api_base=api_base)
    else:
        lm = dspy.LM(model, api_key=api_key)
    
    dspy.configure(lm=lm)

# Initialize DSPy with configuration
configure_dspy()

def load_chart_configs() -> List[Dict[str, Any]]:
    """
    Load all chart configurations from JSON files in the charts directory.
    Returns a list of VisChartConfig objects.
    """
    # Get the project root directory (assuming charts folder is at the project root)
    project_root = Path(__file__).parent.parent.parent
    charts_dir = project_root / "charts"
    
    configs = []
    
    # Check if directory exists
    if not charts_dir.exists() or not charts_dir.is_dir():
        print(f"Warning: Charts directory not found at {charts_dir}")
        return configs
    
    # Process all JSON files
    for chart_file in charts_dir.glob("*.json"):
        try:
            with open(chart_file, 'r') as f:
                chart_data = json.load(f)
                
            # Extract fields
            chart_id = chart_data.get("id", "")
            description = chart_data.get("description", "")
            
            # Extract channel name and type
            channels = []
            if "channels" in chart_data and isinstance(chart_data["channels"], list):
                for channel in chart_data["channels"]:
                    if "name" in channel and "type" in channel:
                        channels.append({
                            "name": channel["name"],
                            "type": channel["type"]
                        })
            # Create chart config dictionary
            if chart_id:
                config = {
                    "id": chart_id,
                    "description": description,
                    "channels": channels
                }
                configs.append(config)
                
        except Exception as e:
            print(f"Error loading chart config from {chart_file}: {e}")
    
    return configs


# Load chart configurations
chart_configs = load_chart_configs()

# VisAnalysis Signature - For analyzing visualization requirements
class VisAnalysisSignature(dspy.Signature):
    """
    Analyze user query and data to determine appropriate visualization from the list of candidates
    """
    query: str = dspy.InputField(desc="User's query about data visualization")
    data_description: str = dspy.InputField(desc="Description of the dataset")
    data_sample: str = dspy.InputField(desc="Sample of the dataset (first few rows)")
    vis_template_candidate: List[Dict[str, Any]] = dspy.InputField(desc="List of visualization template candidates, each containing 'id', 'description', and 'channels' (list of dicts with 'name' and 'type')")
    
    chart_id: str = dspy.OutputField(desc="Recommended chart id from the list of candidates")
    sheet_name: str = dspy.OutputField(desc="The name of the Excel sheet to use for data processing when working with multi-sheet Excel files")
    preprocessing_instructions: str = dspy.OutputField(desc="Instructions for the data preprocessor on how to transform the data for visualization")
    

# DataPreprocesser Signature - For generating data processing code
class DataPreprocesserSignature(dspy.Signature):
    """
    Generate partial pandas code to be inserted into a template based on visualization requirements.
    Do not generate complete code, only the specific data transformation part.
    Keep original column names that maintain the semantic meaning of the data.
    Provide a mapping between original data columns and visualization channel names.
    If previous_error is provided, fix the code to address the error.
    """
    preprocessing_instructions: str = dspy.InputField(desc="Instructions on how to process the data")
    data_description: str = dspy.InputField(desc="Description of the dataset")
    data_sample: str = dspy.InputField(desc="Sample of the dataset (first few rows)")
    code_template: str = dspy.InputField(desc="Template code with placeholders where generated code should be inserted")
    chart_id: str = dspy.InputField(desc="ID of the visualization chart template to use")
    target_channels: List[Dict[str, str]] = dspy.InputField(desc="Target visualization channels that the processed data must provide values for. DO NOT rename columns to match these channel names, instead create a mapping.")
    previous_code: str = dspy.InputField(desc="Previous code that failed to execute correctly", default=None)
    previous_error: str = dspy.InputField(desc="Error message from previous code execution attempt", default=None)
    
    pandas_code: str = dspy.OutputField(desc="Only the specific data transformation code that will be inserted into the template, not complete code. KEEP ORIGINAL COLUMN NAMES that maintain the semantic meaning of the data. If there was a previous error, make sure to fix the issues.")
    channel_mapping: Dict[str, str] = dspy.OutputField(desc="Mapping between visualization channel names (keys) and actual dataframe column names (values). Example: {'category': 'industry_type', 'value': 'energy_consumption'}")

