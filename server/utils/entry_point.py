import traceback
import json
from typing import Dict, Any

from utils.query_analysis import QueryAnalysis
from utils.data_preprocess import DataPreprocesser
from utils.llm_config import load_chart_configs, DataResponseSignature
import dspy
from utils.logger import get_logger, log_dict
import logging
import json
import os
import time
import pandas as pd
from pathlib import Path
from typing import Dict, Any, List
from report.stat_func import get_docx_placeholder_replacement_values, replace_docx_placeholders

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
        self.response_generator = dspy.ChainOfThought(DataResponseSignature)

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
            logger.info(
                f"处理查询: '{query[:50]}...'" if len(query) > 50 else f"处理查询: '{query}'"
            )

            analysis_result = self.query_analyzer.analyze(
                query, data_description, data_sample, self.chart_configs
            )

            logger.info(f"查询分析结果: {analysis_result}")

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
                    # 生成自然语言回答
                response_result = self.generate_response(
                    query=query,
                    processed_results=processed_res["data"],
                )

                # 准备返回结果
                result = {
                    "query_type": "value",
                    "data": processed_res["data"],
                    "response": response_result.get("response", ""),
                }

                logger.info(f"数值查询完成 - 处理了 {len(processed_res['data'])} 条数据")
                return result

            elif query_type == "visualization":  # 处理可视化查询
                # 获取图表信息
                chart_id = analysis_result.get("chart_id")
                chart_title = analysis_result.get("chart_title", "")

                # 查找匹配的图表配置
                target_chart = next(
                    (config for config in self.chart_configs if config["id"] == chart_id), None
                )

                if target_chart:
                    target_channels = target_chart["channels"]
                    channel_names = [c["name"] for c in target_channels]
                    logger.info(
                        f"处理可视化查询 - 图表: {chart_id}, 需要通道: {', '.join(channel_names)}"
                    )
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
                    "chart_title": chart_title,
                    "channel_mapping": channel_mapping,
                }

                # 记录结果信息
                data_count = len(processed_res["data"])
                logger.info(f"可视化查询完成 - 图表: {chart_id}, 处理了 {data_count} 条数据")
                return result

            elif query_type == "report":  # 处理报告生成
                # 获取报告参数
                province = analysis_result.get("province", "湖北")
                year = analysis_result.get("year", "2022")

                # 确保年份是整数
                try:
                    year = int(year)
                except ValueError:
                    logger.error(f"无效的年份格式: {year}")
                    return {"error": f"无效的年份格式: {year}"}

                # 生成报告
                report_path = self.generate_report(data_path, province, year)

                # 检查报告生成结果
                if not report_path or not os.path.exists(report_path):
                    logger.error("报告生成失败")
                    return {"error": "报告生成失败"}

                # 准备返回结果
                result = {
                    "query_type": "report",
                    "report_path": report_path,
                    "province": province,
                    "year": str(year),
                }

                logger.info(f"报告生成完成: {report_path}")
                return result

        except Exception as e:
            import traceback

            error_msg = str(e)
            logger.error(f"处理查询时出现异常: {error_msg}")
            logger.debug(traceback.format_exc())
            return {"error": f"Error processing query: {error_msg}"}

    def generate_report(self, data_path: str, province: str, year: int) -> str:
        try:
            # 记录开始时间
            start_time = time.time()
            logger.info(f"开始生成{province}{year}年能源消费报告...")

            # 加载数据
            logger.info(f"从{data_path}加载数据")
            base_path = Path(data_path).parent if os.path.isfile(data_path) else Path(data_path)
            data_file = base_path / "湖北_外部能耗数据.xlsx"

            if not os.path.exists(data_file):
                logger.error(f"数据文件不存在: {data_file}")
                return None

            # 加载各个数据表
            df1 = pd.read_excel(data_file, sheet_name="hubei_in_y_pro_ind_ene_off")
            df2 = pd.read_excel(data_file, sheet_name="hubei_in_y_pro_ind_ene2_off")
            df3 = pd.read_excel(data_file, sheet_name="hubei_in_y_pro_ind_prd_off")
            df4 = pd.read_excel(data_file, sheet_name="hubei_in_y_pro_gdp_off")

            # 获取报告替换值
            replacement_values = get_docx_placeholder_replacement_values(
                [df1, df2, df3, df4], year=year, province=province
            )

            # 生成报告
            output_path = replace_docx_placeholders(replacement_values)

            # 记录完成时间
            generation_time = time.time() - start_time
            logger.info(f"报告生成完成，耗时: {generation_time:.2f}秒, 路径: {output_path}")

            return output_path

        except Exception as e:
            logger.error(f"生成报告时出错: {str(e)}")
            import traceback

            logger.debug(traceback.format_exc())
            return None

    def generate_response(
        self, query: str, processed_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate a natural language response to explain the data results in context of the user's query.

        Args:
            query: User's original query about data or visualization
            processed_results: Processed data results in DataFrame records format
            chart_id: ID of the visualization chart template used
            channel_mapping: Mapping between visualization channel names and actual dataframe column names

        Returns:
            Dict containing the natural language response and key insights
        """
        try:
            logger.info("生成数据自然语言响应")

            # 限制处理结果的数量，避免响应过大
            sample_results = (
                processed_results[:30] if len(processed_results) > 30 else processed_results
            )

            response = self.response_generator(
                query=query,
                processed_results=sample_results,
            )

            return response
        except Exception as e:
            logger.error(f"生成自然语言响应失败: {str(e)}")
            traceback.print_exc()
            return {
                "response": f"根据您的查询，我们处理了数据，但无法生成详细响应。",
            }
