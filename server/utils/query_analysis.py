import traceback
from typing import Dict, Any, List

import dspy
import json
from utils.llm_config import QueryAnalysisSignature
from utils.logger import get_logger, log_dict

# 获取该模块的日志器
logger = get_logger("query_analysis")

class QueryAnalysis:
    def __init__(self):
        self.module = dspy.ChainOfThought(QueryAnalysisSignature)
    
    def analyze(self, query: str, data_description: str, data_sample: str, vis_template_candidate: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze the user query and data to determine if it's a value query or a visualization query,
        and return appropriate information
        
        Args:
            query: User's query about data or visualization
            data_description: Description of the dataset
            data_sample: Sample of the dataset (first few rows)
            vis_template_candidate: List of visualization template candidates
            
        Returns:
            Dict containing query_type, and other fields depending on the query type:
            - For 'value' queries: sheet_name and preprocessing_instructions
            - For 'visualization' queries: chart_id, sheet_name, and preprocessing_instructions
        """
        logger.info(f"开始分析查询: {query}")
        logger.debug(f"模板候选数量: {len(vis_template_candidate)}")
        
        try:
            logger.info("调用 LLM 进行查询分析")
            response = self.module(
                query=query,
                data_description=data_description,
                data_sample=data_sample,
                vis_template_candidate=vis_template_candidate
            )
            
            # Common fields for both query types
            result = {
                "query_type": response.query_type,
                "sheet_name": response.sheet_name,
                "preprocessing_instructions": response.preprocessing_instructions
            }
            
            # Add fields specific to visualization queries
            if response.query_type == "visualization":
                logger.info(f"查询类型: 可视化, 选择图表ID: {response.chart_id}")
                result.update({
                    "chart_id": response.chart_id
                })
            else:
                logger.info(f"查询类型: 数值")
            
            logger.debug(f"选择工作表: {response.sheet_name}")
            log_dict(logger, "查询分析结果", result)
            
            return result
        except Exception as e:
            logger.error(f"查询分析失败: {str(e)}")
            traceback.print_exc()
            return {
                "error": f"Error analyzing query requirements: {str(e)}"
            }
