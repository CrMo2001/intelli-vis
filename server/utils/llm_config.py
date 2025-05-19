import os
import json
from pathlib import Path
from enum import Enum, auto
from typing import Dict, Any, List, Literal, Optional, Union
from dotenv import load_dotenv
import dspy
from utils.logger import get_logger, log_dict

# 获取该模块的日志器
logger = get_logger("llm_config")

# Load environment variables
logger.info("加载环境变量")
load_dotenv()


# Configure DSPy with OpenAI
def configure_dspy():
    logger.info("配置 DSPy 日志器")
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    logger.info(f"使用模型: {model}")

    # Configure model with optional base URL if specified
    if api_base:
        logger.debug(f"使用自定义 API 基础地址: {api_base}")
        lm = dspy.LM(model, api_key=api_key, api_base=api_base)
    else:
        logger.debug("使用默认 API 基础地址")
        lm = dspy.LM(model, api_key=api_key)

    logger.info("完成 DSPy 配置")
    dspy.configure(lm=lm)


# Initialize DSPy with configuration
logger.info("初始化 DSPy 配置")
configure_dspy()


def load_chart_configs() -> List[Dict[str, Any]]:
    """
    Load all chart configurations from JSON files in the charts directory.
    Returns a list of VisChartConfig objects.
    """
    logger.info("加载图表配置文件")

    # Get the project root directory (assuming charts folder is at the project root)
    project_root = Path(__file__).parent.parent.parent
    charts_dir = project_root / "charts"

    logger.debug(f"图表目录路径: {charts_dir}")
    configs = []

    # Check if directory exists
    if not charts_dir.exists() or not charts_dir.is_dir():
        logger.warning(f"图表目录未找到: {charts_dir}")
        return configs

    # Process all JSON files
    chart_files = list(charts_dir.glob("*.json"))
    logger.info(f"找到 {len(chart_files)} 个图表配置文件")

    for chart_file in chart_files:
        try:
            logger.debug(f"正在加载图表配置: {chart_file.name}")
            with open(chart_file, "r") as f:
                chart_data = json.load(f)

            # Extract fields
            chart_id = chart_data.get("id", "")
            description = chart_data.get("description", "")

            # Extract channel name and type
            channels = []
            if "channels" in chart_data and isinstance(chart_data["channels"], list):
                for channel in chart_data["channels"]:
                    if "name" in channel and "type" in channel:
                        channels.append({"name": channel["name"], "type": channel["type"]})

            # Create chart config dictionary
            if chart_id:
                config = {"id": chart_id, "description": description, "channels": channels}
                configs.append(config)
                logger.debug(f"加载图表: {chart_id}, 通道数: {len(channels)}")
            else:
                logger.warning(f"跳过没有 ID 的图表配置: {chart_file.name}")

        except Exception as e:
            logger.error(f"加载图表配置失败 {chart_file}: {e}")

    return configs


# Load chart configurations
logger.info("加载全局图表配置")
chart_configs = load_chart_configs()
logger.info(f"共加载了 {len(chart_configs)} 个图表配置")


# Define enum classes for type safety
class QueryType(str, Enum):
    VALUE = "value"  # For specific numerical/data value queries
    VISUALIZATION = "visualization"  # For new visualization requests
    REPLACE = "replace"  # For replacing an existing visualization
    REPORT = "report"  # For report generation

# Query Analysis Signature - For analyzing user queries about data or visualizations
class QueryAnalysisSignature(dspy.Signature):
    """
    Analyze user query and data to determine if the user wants a specific value or a visualization,
    and select appropriate processing parameters.
    """

    query: str = dspy.InputField(desc="User's query about data or visualization")
    data_description: str = dspy.InputField(desc="Description of the dataset")
    data_sample: str = dspy.InputField(desc="Sample of the dataset (first few rows)")
    vis_template_candidate: List[Dict[str, Any]] = dspy.InputField(
        desc="List of visualization template candidates, each containing 'id', 'description', and 'channels' (list of dicts with 'name' and 'type')"
    )
    
    # New fields for handling VAST system state and chat history
    vast_system_state: Optional[List[Dict[str, Any]]] = dspy.InputField(
        desc="The current state of the VAST visualization system, including a list of existing visualizations with their IDs, types, titles, and bindings",
        default=None
    )
    message_history: Optional[List[Dict[str, Any]]] = dspy.InputField(
        desc="Previous conversation messages between the user and the system",
        default=None
    )

    query_type: Union[QueryType, Literal["value", "visualization", "replace", "report"]] = dspy.OutputField(
        desc="Type of query: 'value' for specific numerical/data value queries, 'visualization' for new visualization requests, 'replace' for replacing an existing visualization, 'report' for report generation. Only replace the chart when user explicitly asks for it, otherwise create a new one."
    )

    # Fields for visualization queries
    chart_id: str = dspy.OutputField(
        desc="ID of the selected visualization template from vis_template_candidate. Only needed when query_type is 'visualization' or 'replace'. This is NOT the frontend visualization ID, but the template ID."
    )
    chart_title: str = dspy.OutputField(
        desc="Title of the selected visualization template. Only needed when query_type is 'visualization' or 'replace'. Use Chinese for the title. Be short, ignoring unnecesary attributes."
    )
    
    # New field for replacing existing visualizations
    existing_visualization_id: Optional[str] = dspy.OutputField(
        desc="ID of the existing visualization in the frontend to replace. If empty, a new visualization will be created. If not empty, the existing visualization with this ID will be replaced. This is different from chart_id which refers to the template ID.",
        default=""
    )

    # Fields for report generation
    province: str = dspy.OutputField(
        desc="Province name for report generation. Only needed when query_type is 'report'"
    )
    year: str = dspy.OutputField(
        desc="Year for report generation. Only needed when query_type is 'report'"
    )

    # Common fields for both query types
    sheet_name: str = dspy.OutputField(
        desc="The name of the Excel sheet to use for data processing when working with multi-sheet Excel files"
    )
    preprocessing_instructions: str = dspy.OutputField(
        desc="Instructions for the data preprocessor on how to transform the data for the query"
    )


# DataPreprocesser Signature - For generating data processing code
class DataPreprocesserSignature(dspy.Signature):
    """
    Generate partial pandas code to be inserted into a template based on visualization requirements.
    Do not generate complete code, only the specific data transformation part.
    Keep original column names that maintain the semantic meaning of the data.
    Provide a mapping between original data columns and visualization channel names.
    If previous_error is provided, fix the code to address the error.
    """

    preprocessing_instructions: str = dspy.InputField(
        desc="Instructions on how to process the data"
    )
    data_description: str = dspy.InputField(desc="Description of the dataset")
    data_sample: str = dspy.InputField(desc="Sample of the dataset (first few rows)")
    code_template: str = dspy.InputField(
        desc="Template code with placeholders where generated code should be inserted"
    )
    chart_id: str = dspy.InputField(desc="ID of the visualization chart template to use")
    target_channels: List[Dict[str, str]] = dspy.InputField(
        desc="Target visualization channels that the processed data must provide values for. DO NOT rename columns to match these channel names, instead create a mapping."
    )
    previous_code: str = dspy.InputField(
        desc="Previous code that failed to execute correctly", default=None
    )
    previous_error: str = dspy.InputField(
        desc="Error message from previous code execution attempt", default=None
    )

    pandas_code: str = dspy.OutputField(
        desc="Only the specific data transformation code that will be inserted into the template, not complete code. KEEP ORIGINAL COLUMN NAMES that maintain the semantic meaning of the data. If there was a previous error, make sure to fix the issues."
    )
    channel_mapping: Dict[str, str] = dspy.OutputField(
        desc="Mapping between visualization channel names (keys) and actual dataframe column names (values). Example: {'category': 'industry_type', 'value': 'energy_consumption'}"
    )


class DataResponseSignature(dspy.Signature):
    """
    Generate a natural language response to the user based on their query and the processed data results.
    This response should interpret the data in context of the original query and explain key insights.
    """

    query: str = dspy.InputField(desc="User's original query about data or visualization")
    processed_results: List[Dict[str, Any]] = dspy.InputField(
        desc="Processed data results in DataFrame records format"
    )

    response: str = dspy.OutputField(
        desc="Natural language response explaining the data results in context of the user's query. Should be detailed, informative, and directly answer the user's question. You can also add a little bit of insights."
    )
