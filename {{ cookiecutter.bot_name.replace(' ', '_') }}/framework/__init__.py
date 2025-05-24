"""
OpenAutomate Bot Template Framework

This package contains all the core utilities and infrastructure for the OpenAutomate bot template.
Do not modify these files unless you are contributing to the framework itself.
"""

from .base_bot import BaseBot
from .transaction_folders import (
    create_transaction_folders,
    cleanup_transaction_folders,
    get_transaction_folder_path,
    ensure_transaction_folder
)
from .logger_setup import get_logger

__version__ = "1.0.0"
__all__ = [
    "BaseBot",
    "create_transaction_folders",
    "cleanup_transaction_folders", 
    "get_transaction_folder_path",
    "ensure_transaction_folder",
    "get_logger"
] 