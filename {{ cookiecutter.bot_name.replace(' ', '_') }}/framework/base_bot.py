"""
Simple Base Bot Class

Provides basic bot functionality with graceful fallbacks.
"""

import logging
import time
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class BaseBot(ABC):
    """
    Simple base bot class for automation tasks.
    Inherit from this and implement the execute() method.
    """
    
    def __init__(self, bot_name: str, config_path: Optional[str] = None):
        self.bot_name = bot_name
        self.start_time = time.time()
        
        # Setup simple logging
        self.logger = self._setup_simple_logger()
        
        # Try to load optional components
        self.config = self._load_config(config_path)
        self.agent_client = self._setup_agent()
        
        self.logger.info(f"Bot '{self.bot_name}' initialized")
    
    def _setup_simple_logger(self) -> logging.Logger:
        """Setup basic logging"""
        logger = logging.getLogger(self.bot_name)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_config(self, config_path: Optional[str] = None) -> Dict:
        """Load configuration with fallback to defaults"""
        try:
            from config_manager import ConfigManager
            config_manager = ConfigManager(config_path)
            return config_manager.get_config()
        except:
            self.logger.info("Using default configuration (config manager not available)")
            return {
                'bot': {'name': self.bot_name},
                'agent': {'enabled': True, 'host': 'localhost', 'port': 8080},
                'logging': {'level': 'INFO'}
            }
    
    def _setup_agent(self):
        """Setup agent client with graceful fallback"""
        try:
            from openautomateagent import Client as OpenAutomateAgent
            agent_config = self.config.get('agent', {})
            if agent_config.get('enabled', True):
                host = agent_config.get('host', 'localhost')
                port = agent_config.get('port', 8080)
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
            
        return results 