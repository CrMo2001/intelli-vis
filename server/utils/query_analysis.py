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

    def analyze(
        self,
        query: str,
        data_description: str,
        data_sample: str,
        vis_template_candidate: List[Dict[str, Any]],
        vast_system_state: List[Dict[str, Any]] = None,
        message_history: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Analyze the user query and data to determine if it's a value query, visualization query, or replacement query,
        and return appropriate information

        Args:
            query: User's query about data or visualization
            data_description: Description of the dataset
            data_sample: Sample of the dataset (first few rows)
            vis_template_candidate: List of visualization template candidates
            vast_system_state: Current state of the VAST visualization system
            message_history: Previous conversation messages

        Returns:
            Dict containing query_type, and other fields depending on the query type:
            - For 'value' queries: sheet_name and preprocessing_instructions
            - For 'visualization' queries: chart_id, sheet_name, and preprocessing_instructions
            - For 'replace' queries: chart_id, existing_visualization_id, sheet_name, and preprocessing_instructions
            - For 'report' queries: province, year, sheet_name, and preprocessing_instructions
        """
        logger.info(f"开始分析查询: {query}")
        logger.debug(f"模板候选数量: {len(vis_template_candidate)}")

        try:
            logger.info("调用 LLM 进行查询分析")
            response = self.module(
                query=query,
                data_description=data_description,
                data_sample=data_sample,
                vis_template_candidate=vis_template_candidate,
                vast_system_state=vast_system_state,
                message_history=message_history,
            )

            # Common fields for both query types
            result = {
                "query_type": response.query_type,
                "sheet_name": response.sheet_name,
                "preprocessing_instructions": response.preprocessing_instructions,
            }

            # Add fields specific to visualization or replace queries
            if response.query_type == "visualization" or response.query_type == "replace":
                logger.info(f"查询类型: {response.query_type}, 选择图表ID: {response.chart_id}")
                result.update({"chart_id": response.chart_id, "chart_title": response.chart_title})
                
                # 如果是替换查询，添加现有可视化ID
                if response.query_type == "replace" and hasattr(response, "existing_visualization_id"):
                    existing_id = response.existing_visualization_id
                    if existing_id:
                        logger.info(f"将替换前端可视化ID: {existing_id}")
                        result.update({"existing_visualization_id": existing_id})
            elif response.query_type == "report":
                logger.info(f"查询类型: 报告生成, 省份: {response.province}, 年份: {response.year}")
                result.update({"province": response.province, "year": response.year})
            else:
                logger.info(f"查询类型: 数值")

            logger.debug(f"选择工作表: {response.sheet_name}")
            log_dict(logger, "查询分析结果", result)

            return result
        except Exception as e:
            logger.error(f"查询分析失败: {str(e)}")
            traceback.print_exc()
            return {"error": f"Error analyzing query requirements: {str(e)}"}
