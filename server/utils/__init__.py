"""
Main module for intelligent visualization analysis.
This module exports all the classes needed for visualization analysis and data preprocessing.
"""

# Import and re-export classes from their respective modules
from utils.llm_config import configure_dspy, VisAnalysisSignature, DataPreprocesserSignature
from utils.vis_analysis import VisAnalysis
from utils.data_preprocess import DataPreprocesser
from utils.entry_point import EntryPoint

# Initialize DSPy on import
configure_dspy()

__all__ = [
    'VisAnalysisSignature',
    'DataPreprocesserSignature',
    'VisAnalysis',
    'DataPreprocesser',
    'EntryPoint',
]
