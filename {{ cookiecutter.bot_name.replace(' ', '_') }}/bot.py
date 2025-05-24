"""
{{cookiecutter.bot_description}}

Please make sure you install the bot dependencies:
pip install -r requirements.txt

For OpenAutomate platform integration, ensure the OpenAutomate Agent is running.
"""

import sys
import os
from pathlib import Path

# Add framework to path
framework_path = os.path.join(os.path.dirname(__file__), 'framework')
sys.path.insert(0, framework_path)

from base_bot import BaseBot
from transaction_folders import create_transaction_folders, ensure_folder


class Bot(BaseBot):
    """
    {{cookiecutter.bot_name}} - {{cookiecutter.bot_description}}
    
    Just modify the execute() method below to add your automation logic!
    """
    
    def execute(self):
        """
        🤖 Main automation logic - EDIT THIS METHOD!
        
        Add your automation code here:
        - Process files from self.input_folder
        - Save results to self.output_folder  
        - Use self.get_asset('key') for secure data
        - Call self.update_status('message') for progress updates
        """
        self.logger.info("🚀 Starting {{cookiecutter.bot_name}}...")
        
        # Create working folders automatically
        create_transaction_folders(self.bot_name, self.logger)
        input_folder = ensure_folder(self.bot_name, "input")
        output_folder = ensure_folder(self.bot_name, "output")
        
        # Update status (visible in OpenAutomate platform)
        self.update_status("Processing automation tasks...")
        
        # Example: Get secure configuration from platform
        # api_key = self.get_asset('api_key')
        # database_url = self.get_asset('database_url')
        
        # TODO: Add your automation logic here!
        # Examples:
        # - Web scraping (see examples/simple_web_scraper.py)
        # - File processing (see tasks/file_tasks.py)
        # - Email automation (see tasks/email_tasks.py)
        # - API calls (see tasks/web_tasks.py)
        
        # Example: Process files in input folder
        input_files = list(input_folder.glob("*.*"))
        if input_files:
            self.logger.info(f"📁 Found {len(input_files)} files to process")
            for file in input_files:
                self.logger.info(f"📄 Processing: {file.name}")
                # Add your file processing logic here
                # You can use tasks from tasks/ directory
        else:
            self.logger.info("📂 No files found in input folder")
            self.logger.info(f"💡 Add files to: {input_folder}")
        
        self.update_status("Automation completed")
        self.logger.info("✅ {{cookiecutter.bot_name}} completed!")
        
        return {
            'message': '✅ Automation completed successfully!',
            'data': {
                'items_processed': len(input_files),
                'files_created': 0
            }
        }


# Run the bot
if __name__ == "__main__":
    print("🚀 Starting {{cookiecutter.bot_name}}...")
    
    # Create and run bot
    bot = Bot("{{cookiecutter.bot_name}}")
    results = bot.run()
    
    # Print results
    if results['success']:
        print(f"✅ SUCCESS: {results['message']}")
        print(f"⏱️  Completed in {results['execution_time']:.2f} seconds")
    else:
        print(f"❌ FAILED: {results['message']}")
    
    print("👋 Bot finished!") 