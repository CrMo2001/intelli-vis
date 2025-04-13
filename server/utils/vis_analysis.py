import traceback
from typing import Dict, Any, List

import dspy
from utils.llm_config import VisAnalysisSignature

class VisAnalysis:
    def __init__(self):
        self.module = dspy.ChainOfThought(VisAnalysisSignature)
    
    def analyze(self, query: str, data_description: str, data_sample: str, vis_template_candidate: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the user query and data to determine visualization requirements
        
        Args:
            query: User's query about data visualization
            data_description: Description of the dataset
            data_sample: Sample of the dataset (first few rows)
            vis_template_candidate: List of visualization template candidates
            
        Returns:
            Dict containing chart_id, sheet_name, and preprocessing instructions
        """
        try:
            response = self.module(
                query=query,
                data_description=data_description,
                data_sample=data_sample,
                vis_template_candidate=vis_template_candidate
            )
            
            return {
                "chart_id": response.chart_id,
                "sheet_name": response.sheet_name,
                "preprocessing_instructions": response.preprocessing_instructions
            }
        except Exception as e:
            traceback.print_exc()
            return {
                "error": f"Error analyzing visualization requirements: {str(e)}"
            }
