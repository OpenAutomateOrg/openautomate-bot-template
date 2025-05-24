"""
Simple Base Bot Class

Provides basic bot functionality with graceful fallbacks.
"""

import logging
import time
import configparser
from pathlib import Path
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime


class BaseBot(ABC):
    """
    Simple base bot class for automation tasks.
    Inherit from this and implement the execute() method.
    """
    
    def __init__(self, bot_name: str, config_path: Optional[str] = None):
        self.bot_name = bot_name
        self.start_time = time.time()
        
        # Load config first
        self.config = self._load_config(config_path)
        
        # Setup logging with file output
        self.logger = self._setup_logging()
        
        # Setup agent
        self.agent_client = self._setup_agent()
        
        self.logger.info(f"Bot '{self.bot_name}' initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging with both console and file output"""
        logger = logging.getLogger(self.bot_name)
        
        # Clear any existing handlers
        logger.handlers.clear()
        
        # Set log level
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler - write to logs folder
        try:
            from transaction_folders import get_base_path_from_config
            base_path = get_base_path_from_config(self.bot_name)
            logs_folder = base_path / "logs"
            logs_folder.mkdir(parents=True, exist_ok=True)
            
            # Create log file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_folder / f"{self.bot_name}_{timestamp}.log"
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
            # Also create a "latest.log" file that gets overwritten each run
            latest_log_file = logs_folder / f"{self.bot_name}_latest.log"
            latest_handler = logging.FileHandler(latest_log_file, mode='w', encoding='utf-8')
            latest_handler.setFormatter(formatter)
            logger.addHandler(latest_handler)
            
            logger.info(f"📝 Logging to: {log_file}")
            
        except Exception as e:
            # If file logging fails, just continue with console logging
            logger.warning(f"Could not setup file logging: {e}")
        
        return logger
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration from config.ini with fallback to defaults"""
        try:
            # Try to find config.ini
            if config_path:
                config_file = Path(config_path)
            else:
                config_file = Path(__file__).parent.parent / "config" / "config.ini"
            
            if config_file.exists():
                config = configparser.ConfigParser()
                config.read(config_file)
                
                # Convert to dictionary
                config_dict = {}
                for section in config.sections():
                    config_dict[section] = dict(config[section])
                
                return config_dict
            else:
                print("Config file not found, using defaults")
                
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
        
        # Fallback defaults
        return {
            'bot': {'name': self.bot_name},
            'agent': {'enabled': 'true', 'host': 'localhost', 'port': '8080'},
            'logging': {'level': 'INFO'},
            'folders': {'base_path': 'Documents/openautomatebot', 'subfolder_names': 'input,output,temp,screenshots,logs'}
        }
    
    def _setup_agent(self):
        """Setup agent client with graceful fallback"""
        try:
            from openautomateagent import Client as OpenAutomateAgent
            agent_config = self.config.get('agent', {})
            if agent_config.get('enabled', 'true').lower() == 'true':
                host = agent_config.get('host', 'localhost')
                port = int(agent_config.get('port', 8080))
                client = OpenAutomateAgent(host=host, port=port)
                self.logger.info(f"Connected to OpenAutomate Agent at {host}:{port}")
                return client
        except Exception as e:
            self.logger.info(f"Agent not available: {e}")
        return None
    
    def get_asset(self, key: str) -> Optional[str]:
        """Get asset from agent (returns None if not available)"""
        if not self.agent_client:
            return None
        
        try:
            return self.agent_client.get_asset(key)
        except Exception as e:
            self.logger.debug(f"Could not get asset '{key}': {e}")
            return None
    
    def get_all_asset_keys(self) -> list:
        """Get all asset keys (returns empty list if not available)"""
        if not self.agent_client:
            return []
        
        try:
            return self.agent_client.get_all_asset_keys()
        except Exception as e:
            self.logger.debug(f"Could not get asset keys: {e}")
            return []
    
    def update_status(self, status: str) -> bool:
        """Update status via agent (does nothing if not available)"""
        if not self.agent_client:
            self.logger.info(f"Status: {status}")
            return False
        
        try:
            return self.agent_client.update_status(status)
        except Exception as e:
            self.logger.debug(f"Could not update status: {e}")
            return False
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Implement your automation logic here.
        Return a dictionary with your results.
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Run the bot with error handling.
        """
        results = {
            'success': False,
            'message': '',
            'data': {},
            'execution_time': 0
        }
        
        try:
            self.logger.info(f"Starting {self.bot_name}")
            
            # Run your automation
            execution_results = self.execute()
            
            # Update results
            if isinstance(execution_results, dict):
                results.update(execution_results)
            
            results['success'] = True
            if not results.get('message'):
                results['message'] = 'Automation completed successfully'
            
            self.logger.info("Automation completed successfully")
            
        except Exception as e:
            error_msg = f"Error during automation: {str(e)}"
            self.logger.error(error_msg)
            results['success'] = False
            results['message'] = error_msg
            
        finally:
            # Calculate execution time
            results['execution_time'] = time.time() - self.start_time
            self.logger.info(f"Execution completed in {results['execution_time']:.2f} seconds")
            
        return results 