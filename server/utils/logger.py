import logging
import sys
from typing import Dict, Any


# ANSI color codes
class Colors:
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


# Component colors configuration
COMPONENT_COLORS = {
    "query_analysis": Colors.BLUE,
    "data_preprocess": Colors.GREEN,
    "entry_point": Colors.YELLOW,
    "app": Colors.MAGENTA,
    "llm_config": Colors.CYAN,
    "default": Colors.WHITE,
}


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors based on the component name"""

    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)

    def format(self, record):
        # Get the appropriate color for the component
        component_name = record.name.split(".")[-1]
        color = COMPONENT_COLORS.get(component_name, COMPONENT_COLORS["default"])

        # Add the color to the log level
        level_name = record.levelname
        colored_level = f"{color}{level_name}{Colors.RESET}"
        record.levelname = colored_level

        # Format the message
        result = super().format(record)

        # Add component color to the whole message
        return f"{color}{result}{Colors.RESET}"


def get_logger(name: str) -> logging.Logger:
    """
    Get a configured logger with the specified name.

    Args:
        name: Name of the logger, typically the component name

    Returns:
        A configured logger instance with colored output
    """
    logger = logging.getLogger(name)

    # Only configure the logger if it hasn't been configured yet
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Create a handler that writes to stderr
        handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(logging.INFO)

        # Create a formatter with colors
        formatter = ColoredFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(handler)

    return logger


def log_dict(
    logger: logging.Logger, title: str, data: Dict[str, Any], level: int = logging.DEBUG
) -> None:
    """
    Log a dictionary in a formatted way

    Args:
        logger: The logger to use
        title: Title for the dictionary data
        data: Dictionary to log
        level: Logging level (default: DEBUG)
    """
    import json

    log_message = f"\n{title}:\n"
    log_message += json.dumps(data, indent=4, ensure_ascii=False)

    logger.log(level, log_message)
