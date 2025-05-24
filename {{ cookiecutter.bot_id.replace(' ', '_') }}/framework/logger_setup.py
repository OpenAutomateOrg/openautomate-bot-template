import os
import logging
import logging.handlers
from datetime import datetime
from typing import Dict, Any, Optional


class LoggerSetup:
    """
    Provides standardized logging setup for OpenAutomate bots.
    """
    
    def __init__(self, bot_name: str, config: Dict[str, Any]):
        self.bot_name = bot_name
        self.config = config
        self.logger = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup the logger with file and console handlers."""
        # Get logging configuration
        log_config = self.config.get('logging', {})
        
        # Create logger
        self.logger = logging.getLogger(self.bot_name)
        self.logger.setLevel(getattr(logging, log_config.get('level', 'INFO')))
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(
            log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        
        # Console handler
        if log_config.get('console_enabled', True):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # File handler
        if log_config.get('file_enabled', True):
            log_dir = self._ensure_log_directory()
            log_file = os.path.join(log_dir, f"{self.bot_name}_{datetime.now().strftime('%Y%m%d')}.log")
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=log_config.get('max_file_size', 10*1024*1024),  # 10MB
                backupCount=log_config.get('backup_count', 5)
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def _ensure_log_directory(self) -> str:
        """Ensure the log directory exists."""
        log_dir = self.config.get('logging', {}).get('log_directory', './logs')
        
        # Create absolute path
        if not os.path.isabs(log_dir):
            log_dir = os.path.join(os.path.dirname(__file__), '..', log_dir)
        
        log_dir = os.path.abspath(log_dir)
        os.makedirs(log_dir, exist_ok=True)
        
        return log_dir
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger."""
        return self.logger
    
    def get_timestamp(self) -> datetime:
        """Get current timestamp."""
        return datetime.now()
    
    def log_execution_start(self, additional_info: Optional[Dict[str, Any]] = None):
        """Log the start of bot execution."""
        info = additional_info or {}
        self.logger.info(f"=== Bot Execution Started ===")
        self.logger.info(f"Bot Name: {self.bot_name}")
        self.logger.info(f"Start Time: {self.get_timestamp()}")
        
        for key, value in info.items():
            self.logger.info(f"{key}: {value}")
        
        self.logger.info("=" * 50)
    
    def log_execution_end(self, success: bool, duration: float, additional_info: Optional[Dict[str, Any]] = None):
        """Log the end of bot execution."""
        info = additional_info or {}
        self.logger.info("=" * 50)
        self.logger.info(f"=== Bot Execution Completed ===")
        self.logger.info(f"Bot Name: {self.bot_name}")
        self.logger.info(f"Success: {success}")
        self.logger.info(f"Duration: {duration:.2f} seconds")
        self.logger.info(f"End Time: {self.get_timestamp()}")
        
        for key, value in info.items():
            self.logger.info(f"{key}: {value}")
        
        self.logger.info("=" * 50)


class LoggerError(Exception):
    """Custom exception for logger errors."""
    pass


def get_logger(bot_name: str, level: str = 'INFO') -> logging.Logger:
    """
    Simple standalone function to get a logger for basic use cases.
    
    Args:
        bot_name: Name of the bot/logger
        level: Logging level (default: INFO)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(bot_name)
    
    # Only configure if not already configured
    if not logger.handlers:
        logger.setLevel(getattr(logging, level.upper()))
        
        # Create console handler with simple format
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger 