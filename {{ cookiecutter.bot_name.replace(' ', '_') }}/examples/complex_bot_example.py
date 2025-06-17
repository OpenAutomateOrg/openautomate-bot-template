"""
Complex Bot Example

Demonstrates how to create a sophisticated automation bot using multiple task modules.
This bot performs file processing, web scraping, and email reporting.
"""

import sys
import os
from pathlib import Path

# Add framework and tasks to path
framework_path = os.path.join(os.path.dirname(__file__), '..', 'framework')
tasks_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, framework_path)
sys.path.insert(0, tasks_path)

from base_bot import BaseBot
from transaction_folders import create_transaction_folders, ensure_folder

# Import task modules
try:
    from tasks import file_tasks, web_tasks, email_tasks
    TASKS_AVAILABLE = True
except ImportError as e:
    print(f"Task modules not available: {e}")
    TASKS_AVAILABLE = False


class ComplexAutomationBot(BaseBot):
    """
    Complex automation bot that demonstrates multiple task orchestration.
    
    This bot:
    1. Processes files in the input folder
    2. Scrapes data from websites
    3. Organizes downloaded files
    4. Sends email reports
    5. Cleans up old files
    """
    
    def execute(self):
        """
        Main workflow - orchestrate all automation tasks.
        """
        self.logger.info("Starting complex automation workflow...")

        if not TASKS_AVAILABLE:
            return {
                'message': 'Task modules not available. Please check imports.',
                'data': {'error': 'Missing task modules'}
            }

        # Create working folders
        create_transaction_folders(self.bot_name, self.logger)
        input_folder = ensure_folder(self.bot_name, "input")
        output_folder = ensure_folder(self.bot_name, "output")
        temp_folder = ensure_folder(self.bot_name, "temp")

        # Initialize results tracking
        results = {
            'message': 'Complex automation completed successfully!',
            'data': {
                'tasks_completed': [],
                'files_processed': 0,
                'websites_scraped': 0,
                'files_organized': 0,
                'emails_sent': 0,
                'files_cleaned': 0,
                'errors': []
            }
        }
        
        try:
            # Task 1: Process CSV files
            self.update_status("Processing CSV files...")
            files_processed = self._process_csv_files(input_folder, output_folder)
            results['data']['files_processed'] = files_processed
            if files_processed > 0:
                results['data']['tasks_completed'].append('csv_processing')
            
            # Task 2: Convert text files
            self.update_status("Converting text files...")
            text_files_converted = self._convert_text_files(input_folder, output_folder)
            if text_files_converted > 0:
                results['data']['tasks_completed'].append('text_conversion')
            
            # Task 3: Web scraping
            self.update_status("Scraping websites...")
            scraped_data = self._scrape_websites(output_folder)
            if scraped_data:
                results['data']['websites_scraped'] = len(scraped_data)
                results['data']['tasks_completed'].append('web_scraping')
            
            # Task 4: Check website status
            self.update_status("Checking website status...")
            status_results = self._check_website_status()
            if status_results:
                results['data']['tasks_completed'].append('status_check')
            
            # Task 5: Organize files
            self.update_status("Organizing files...")
            files_organized = self._organize_files(temp_folder)
            results['data']['files_organized'] = files_organized
            if files_organized > 0:
                results['data']['tasks_completed'].append('file_organization')
            
            # Task 6: Send email reports
            self.update_status("Sending email reports...")
            emails_sent = self._send_email_reports(results['data'])
            results['data']['emails_sent'] = emails_sent
            if emails_sent > 0:
                results['data']['tasks_completed'].append('email_reports')
            
            # Task 7: Cleanup old files
            self.update_status("Cleaning up old files...")
            files_cleaned = self._cleanup_old_files(temp_folder)
            results['data']['files_cleaned'] = files_cleaned
            if files_cleaned > 0:
                results['data']['tasks_completed'].append('cleanup')
            
        except Exception as e:
            error_msg = f"Error in complex workflow: {str(e)}"
            self.logger.error(error_msg)
            results['data']['errors'].append(error_msg)
            results['message'] = f'Complex automation failed: {str(e)}'
            raise

        # Final status update
        completed_tasks = len(results['data']['tasks_completed'])
        self.update_status(f"Completed {completed_tasks} automation tasks")

        self.logger.info("Complex automation workflow finished!")
        return results
    
    def _process_csv_files(self, input_folder, output_folder):
        """Process CSV files using file_tasks module"""
        try:
            return file_tasks.process_csv_files(self.logger, input_folder, output_folder)
        except Exception as e:
            self.logger.error(f"CSV processing failed: {e}")
            return 0
    
    def _convert_text_files(self, input_folder, output_folder):
        """Convert text files using file_tasks module"""
        try:
            return file_tasks.convert_text_files_to_uppercase(self.logger, input_folder, output_folder)
        except Exception as e:
            self.logger.error(f"Text conversion failed: {e}")
            return 0
    
    def _scrape_websites(self, output_folder):
        """Scrape websites using web_tasks module"""
        try:
            # Get URLs from assets or use defaults
            urls_to_scrape = []
            
            # Try to get URLs from assets
            scraper_urls = self.get_asset('scraper_urls')
            if scraper_urls:
                if isinstance(scraper_urls, str):
                    urls_to_scrape = [scraper_urls]
                else:
                    urls_to_scrape = scraper_urls
            else:
                # Default URLs for demonstration
                urls_to_scrape = [
                    'https://httpbin.org/html',
                    'https://example.com'
                ]
            
            scraped_data = []
            for url in urls_to_scrape:
                try:
                    data = web_tasks.scrape_website(self.logger, url, output_folder)
                    scraped_data.append(data)
                except Exception as e:
                    self.logger.error(f"Failed to scrape {url}: {e}")
            
            return scraped_data
            
        except Exception as e:
            self.logger.error(f"Web scraping failed: {e}")
            return []
    
    def _check_website_status(self):
        """Check website status using web_tasks module"""
        try:
            # Get URLs to check from assets or use defaults
            urls_to_check = []
            
            status_urls = self.get_asset('status_check_urls')
            if status_urls:
                if isinstance(status_urls, str):
                    urls_to_check = [status_urls]
                else:
                    urls_to_check = status_urls
            else:
                # Default URLs for demonstration
                urls_to_check = [
                    'https://google.com',
                    'https://github.com',
                    'https://stackoverflow.com'
                ]
            
            return web_tasks.check_website_status(self.logger, urls_to_check)
            
        except Exception as e:
            self.logger.error(f"Website status check failed: {e}")
            return None
    
    def _organize_files(self, folder_path):
        """Organize files using file_tasks module"""
        try:
            return file_tasks.organize_files_by_type(self.logger, folder_path)
        except Exception as e:
            self.logger.error(f"File organization failed: {e}")
            return 0
    
    def _send_email_reports(self, report_data):
        """Send email reports using email_tasks module"""
        try:
            # Get email configuration from assets
            smtp_config = {
                'server': self.get_asset('smtp_server') or 'smtp.gmail.com',
                'port': 587,
                'username': self.get_asset('email_username'),
                'password': self.get_asset('email_password'),
                'from_email': self.get_asset('from_email')
            }
            
            # Get recipients from assets
            recipients = self.get_asset('report_recipients')
            if not recipients:
                recipients = 'admin@company.com'  # Default recipient
            
            # Check if we have email credentials
            if not smtp_config['username'] or not smtp_config['password']:
                self.logger.info("Email credentials not configured, skipping email reports")
                return 0
            
            # Add bot name to report data
            report_data_with_bot = {
                'bot_name': self.bot_name,
                'success': True,
                'execution_time': 0,  # Will be updated by base bot
                'data': report_data
            }
            
            return email_tasks.send_report_email(
                self.logger, 
                smtp_config, 
                recipients, 
                report_data_with_bot
            )
            
        except Exception as e:
            self.logger.error(f"Email reporting failed: {e}")
            return 0
    
    def _cleanup_old_files(self, folder_path):
        """Clean up old files using file_tasks module"""
        try:
            # Clean files older than 7 days
            days_old = int(self.get_asset('cleanup_days') or 7)
            return file_tasks.cleanup_old_files(self.logger, folder_path, days_old)
        except Exception as e:
            self.logger.error(f"File cleanup failed: {e}")
            return 0


# Standalone execution
if __name__ == "__main__":
    print("Starting Complex Automation Bot...")
    print("This bot demonstrates multiple task orchestration:")
    print("   - File processing (CSV and text)")
    print("   - Web scraping and status checking")
    print("   - File organization")
    print("   - Email reporting")
    print("   - Automated cleanup")
    print()

    # Load config to get bot name
    try:
        from config_manager import ConfigManager
        config_manager = ConfigManager()
        bot_name = config_manager.get('bot.name', 'ComplexBot')
        print(f"Using bot name from config: {bot_name}")
    except Exception as e:
        print(f"Could not load config, using default name: {e}")
        bot_name = 'ComplexBot'
    
    # Create and run complex bot
    bot = ComplexAutomationBot(bot_name)
    results = bot.run()
    
    # Print detailed results
    print("\n" + "="*50)
    if results['success']:
        print(f"SUCCESS: {results['message']}")
        print(f"Tasks completed: {', '.join(results['data']['tasks_completed'])}")
        print(f"Files processed: {results['data']['files_processed']}")
        print(f"Websites scraped: {results['data']['websites_scraped']}")
        print(f"Files organized: {results['data']['files_organized']}")
        print(f"Emails sent: {results['data']['emails_sent']}")
        print(f"Files cleaned: {results['data']['files_cleaned']}")
        print(f"Completed in {results['execution_time']:.2f} seconds")
    else:
        print(f"FAILED: {results['message']}")
        if results['data']['errors']:
            print(f"Errors: {', '.join(results['data']['errors'])}")

    print("Complex bot finished!")
    print("\nTips:")
    print("   - Add CSV files to input folder to see processing")
    print("   - Configure email assets for reporting")
    print("   - Check output folder for results")
    print("   - Customize URLs in assets for scraping")