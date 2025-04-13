import traceback
import json
from typing import Dict, Any

from utils.vis_analysis import VisAnalysis
from utils.data_preprocess import DataPreprocesser
from utils.llm_config import load_chart_configs


class EntryPoint:
    """
    Main entry point for handling data visualization queries.
    Orchestrates the flow between visualization analysis and data preprocessing.
    """

    def __init__(self):
        self.vis_analyzer = VisAnalysis()
        self.data_preprocesser = DataPreprocesser()
        self.chart_configs = load_chart_configs()
        print(self.chart_configs)

    def process_query(
        self,
        query: str,
        data_path: str,
        data_description: str,
        data_sample: str,
        code_template: str = None,
    ) -> Dict[str, Any]:
        """
        Process a user query by analyzing visualization requirements and processing data accordingly

        Args:
            query: User's query about data visualization
            data_path: Path to the dataset file
            data_description: Description of the dataset
            data_sample: Sample of the dataset (first few rows)
            code_template: Optional template for code generation

        Returns:
            Dict containing processed data and visualization metadata
        """
        try:
            # Step 1: Analyze the visualization requirements
            vis_analysis = self.vis_analyzer.analyze(
                query, data_description, data_sample, self.chart_configs
            )

            print(json.dumps(vis_analysis, indent=4, ensure_ascii=False))

            # Check for errors in visualization analysis
            if "error" in vis_analysis:
                return vis_analysis

            # Step 2: Use the automatic retry process that generates, executes, and retries on failure
            # This replaces the separate generate_code and execute_code steps
            processed_res = self.data_preprocesser.process_with_retry(
                preprocessing_instructions=vis_analysis["preprocessing_instructions"],
                data_description=data_description,
                data_sample=data_sample,
                data_path=data_path,
                sheet_name=vis_analysis.get("sheet_name"),
                code_template=code_template,
                chart_id=vis_analysis["chart_id"],
                # Find the target chart config based on chart_id
                target_channels=[
                    channel
                    for config in self.chart_configs
                    if config["id"] == vis_analysis["chart_id"]
                    for channel in config["channels"]
                ],
                max_attempts=3,  # Set maximum retry attempts
            )
            
            # Return the processed data, chart_id, and channel_mapping
            return {
                "data": processed_res["data"],
                "chart_id": vis_analysis["chart_id"],
                "channel_mapping": processed_res.get("channel_mapping", {}),
            }

        except Exception as e:
            traceback.print_exc()
            return {"error": f"Error processing query: {str(e)}"}
