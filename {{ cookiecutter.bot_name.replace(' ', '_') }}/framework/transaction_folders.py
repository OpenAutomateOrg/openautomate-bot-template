"""
Simple Transaction Folders

Creates folders for automation bots in Documents/automationlab.
"""

import shutil
import logging
from pathlib import Path


def get_simple_logger(name: str) -> logging.Logger:
    """Get a simple logger"""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger


def create_transaction_folders(bot_name, logger=None):
    """
    Create transaction folders for the bot in Documents/automationlab.

    Args:
        bot_name (str): Name of the bot
        logger: Logger instance (optional)
    """
    if logger is None:
        logger = get_simple_logger(bot_name)

    try:
        # Create bot folder in Documents/automationlab
        base_path = Path.home() / "Documents" / "automationlab" / bot_name
        
        # Folder types to create
        folders = ["input", "output", "temp", "screenshots"]

        for folder_name in folders:
            folder_path = base_path / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created folder: {folder_path}")

    except Exception as e:
        logger.error(f"❌ Error creating folders: {e}")
        raise


def cleanup_transaction_folders(bot_name, logger=None):
    """
    Clean up transaction folder contents.

    Args:
        bot_name (str): Name of the bot
        logger: Logger instance (optional)
    """
    if logger is None:
        logger = get_simple_logger(bot_name)

    try:
        base_path = Path.home() / "Documents" / "automationlab" / bot_name
        
        # Clean these folders
        folders_to_clean = ["output", "temp"]

        for folder_name in folders_to_clean:
            folder_path = base_path / folder_name
            if folder_path.exists():
                for item in folder_path.iterdir():
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                logger.info(f"🧹 Cleaned folder: {folder_path}")

    except Exception as e:
        logger.error(f"❌ Error cleaning folders: {e}")


def get_folder_path(bot_name, folder_type="output"):
    """
    Get path to a specific folder.

    Args:
        bot_name (str): Name of the bot
        folder_type (str): Type of folder (input, output, temp, screenshots)

    Returns:
        Path: Path to the folder
    """
    return Path.home() / "Documents" / "automationlab" / bot_name / folder_type


def ensure_folder(bot_name, folder_type="output"):
    """
    Make sure a folder exists and return its path.

    Args:
        bot_name (str): Name of the bot
        folder_type (str): Type of folder

    Returns:
        Path: Path to the folder
    """
    folder_path = get_folder_path(bot_name, folder_type)
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path 