import traceback
import json
from typing import Dict, Any

from utils.query_analysis import QueryAnalysis
from utils.data_preprocess import DataPreprocesser
from utils.llm_config import load_chart_configs
from utils.logger import get_logger, log_dict

# 获取该模块的日志器
logger = get_logger("entry_point")


class EntryPoint:
    """
    Main entry point for handling data visualization queries.
    Orchestrates the flow between visualization analysis and data preprocessing.
    """

    def __init__(self):
        logger.info("初始化 EntryPoint 组件")
        self.query_analyzer = QueryAnalysis()
        self.data_preprocesser = DataPreprocesser()
        
        logger.info("加载图表配置")
        self.chart_configs = load_chart_configs()
        logger.debug(f"加载了 {len(self.chart_configs)} 个图表配置")
        log_dict(logger, "图表配置", self.chart_configs)

    def process_query(
        self,
        query: str,
        data_path: str,
        data_description: str,
        data_sample: str,
        code_template: str = None,
    ) -> Dict[str, Any]:
        """
        Process a user query by analyzing if it's a value query or visualization query,
        and processing data accordingly

        Args:
            query: User's query about data or visualization
            data_path: Path to the dataset file
            data_description: Description of the dataset
            data_sample: Sample of the dataset (first few rows)
            code_template: Optional template for code generation

        Returns:
            Dict containing processed data and appropriate metadata based on query type
        """
        try:
            # 分析查询
            logger.info(f"处理查询: '{query[:50]}...'" if len(query) > 50 else f"处理查询: '{query}'")
            
            analysis_result = self.query_analyzer.analyze(
                query, data_description, data_sample, self.chart_configs
            )

            # 检查错误
            if "error" in analysis_result:
                logger.error(f"查询分析失败: {analysis_result['error']}")
                return analysis_result

            # 获取查询类型
            query_type = analysis_result.get("query_type", "visualization")  # 默认为可视化
            sheet_name = analysis_result.get("sheet_name")
            logger.info(f"查询类型: {query_type}, 使用工作表: {sheet_name}")

            # 处理数值查询
            if query_type == "value":
                logger.info("处理数值查询 - 生成数据处理代码")
                
                processed_res = self.data_preprocesser.process_with_retry(
                    preprocessing_instructions=analysis_result["preprocessing_instructions"],
                    data_description=data_description,
                    data_sample=data_sample,
                    data_path=data_path,
                    sheet_name=sheet_name,
                    code_template=code_template,
                    chart_id=None,  # 数值查询不需要图表
                    target_channels=[],  # 数值查询不需要通道
                    max_attempts=3,
                )
                
                # 检查处理结果
                if "error" in processed_res:
                    logger.error(f"数据处理失败: {processed_res.get('error')}")
                    return processed_res
                
                result = {
                    "query_type": "value",
                    "data": processed_res["data"],
                }
                
                logger.info(f"数值查询完成 - 处理了 {len(processed_res['data'])} 条数据")
                return result

            else:  # 处理可视化查询
                # 获取图表信息
                chart_id = analysis_result.get("chart_id")
                
                # 查找匹配的图表配置
                target_chart = next(
                    (config for config in self.chart_configs if config["id"] == chart_id), None
                )
                
                if target_chart:
                    target_channels = target_chart["channels"]
                    channel_names = [c['name'] for c in target_channels]
                    logger.info(f"处理可视化查询 - 图表: {chart_id}, 需要通道: {', '.join(channel_names)}")
                else:
                    logger.warning(f"处理可视化查询 - 未找到匹配图表: {chart_id}")
                    target_channels = []

                # 生成和执行数据处理代码
                processed_res = self.data_preprocesser.process_with_retry(
                    preprocessing_instructions=analysis_result["preprocessing_instructions"],
                    data_description=data_description,
                    data_sample=data_sample,
                    data_path=data_path,
                    sheet_name=sheet_name,
                    code_template=code_template,
                    chart_id=chart_id,
                    target_channels=target_channels,
                    max_attempts=3,
                )
                
                # 检查处理结果
                if "error" in processed_res:
                    logger.error(f"数据处理失败: {processed_res.get('error')}")
                    return processed_res
                
                # 准备返回结果
                channel_mapping = processed_res.get("channel_mapping", {})
                result = {
                    "query_type": "visualization",
                    "data": processed_res["data"],
                    "chart_id": chart_id,
                    "channel_mapping": channel_mapping,
                }
                
                # 记录结果信息
                data_count = len(processed_res["data"])
                logger.info(f"可视化查询完成 - 图表: {chart_id}, 处理了 {data_count} 条数据")
                return result

        except Exception as e:
            import traceback
            error_msg = str(e)
            logger.error(f"处理查询时出现异常: {error_msg}")
            logger.debug(traceback.format_exc())
            return {"error": f"Error processing query: {error_msg}"}
