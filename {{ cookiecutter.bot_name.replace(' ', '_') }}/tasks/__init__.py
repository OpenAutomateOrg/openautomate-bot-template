"""
Automation Tasks Package

Organize your complex automation logic into focused modules.
"""

from pathlib import Path

def get_task_folder():
    """Get the tasks folder path"""
    return Path(__file__).parent

# Common utilities that all task modules might need
def log_task_start(logger, task_name):
    """Log the start of a task"""
    logger.info(f"🚀 Starting task: {task_name}")

def log_task_complete(logger, task_name, result=None):
    """Log the completion of a task"""
    if result:
        logger.info(f"✅ Task completed: {task_name} - {result}")
    else:
        logger.info(f"✅ Task completed: {task_name}")

def log_task_error(logger, task_name, error):
    """Log a task error"""
    logger.error(f"❌ Task failed: {task_name} - {error}") 