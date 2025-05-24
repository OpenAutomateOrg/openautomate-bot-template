# OpenAutomate Bot Template

A **cookiecutter template** for creating Python automation bots. This template helps you quickly generate a new bot project with all the necessary structure and utilities.

## 🍪 Using This Template (Cookiecutter)

### Prerequisites

Install cookiecutter if you haven't already:
```bash
pip install cookiecutter
```

### Create a New Bot Project

1. **Generate from template**:
   ```bash
   cookiecutter https://github.com/OpenAutomateOrg/openautomate-bot-template
   # OR if you have this locally:
   cookiecutter d:\CapstoneProject\openautomate-bot-template
   ```

2. **Answer the prompts**:
   ```
   bot_name [MyBot]: FileProcessorBot
   bot_description [A Python automation bot]: Processes CSV files automatically
   ```

3. **Navigate to your new project**:
   ```bash
   cd FileProcessorBot
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Edit and run your bot**:
   ```bash
   # Edit the main bot file
   # Then run:
   python bot.py
   ```

## 📁 Generated Project Structure

After using cookiecutter, you'll get a project like this:

```
your-bot-project/
├── bot.py                     # 👈 Your main file - edit this!
├── framework/                 # Bot utilities (don't touch)
├── examples/                  # Example bots to learn from
├── config/                    # Configuration files
├── tasks/                     # Your custom task modules (optional)
├── requirements.txt           # Python dependencies
├── .gitignore                # Git ignore file
└── README.md                  # Project-specific README
```

## 🚀 Quick Start (After Creating Your Bot)

1. **Edit bot.py** - Add your automation logic to the `execute` method
2. **Run** with: `python bot.py`
3. **Check results** in `Documents/openautomate-bot/YourBotName/`

That's it! 🎉

## 🛠️ Template Development

If you're contributing to this template itself:

### Template Structure
```
openautomate-bot-template/
├── cookiecutter.json          # Template configuration
├── {{cookiecutter.project_slug}}/  # Template files
│   ├── bot.py
│   ├── framework/
│   ├── config/
│   └── ...
├── hooks/                     # Pre/post generation scripts
└── README.md                  # This file
```

### Testing the Template
```bash
# Test template generation
cookiecutter . --no-input

# Test with custom values
cookiecutter . --no-input bot_name="TestBot" bot_description="Test automation bot"
```

---

# 📖 Bot Development Guide

*The following sections apply to bots created FROM this template*

## 💡 How to Use Your Generated Bot

### Step 1: Edit bot.py

Open `bot.py` and find the `execute` method. Add your automation code:

```python
def execute(self):
    """
    Add your automation code here!
    """
    self.logger.info("🤖 Starting my automation...")
    
    # Example: Get data from platform
    api_key = self.get_asset('api_key')  # Get secure data
    
    # Example: Create folders for your files
    create_transaction_folders(self.bot_name, self.logger)
    
    # TODO: Your automation code here!
    # - Process files
    # - Scrape websites  
    # - Automate tasks
    # - Send emails
    # - Anything you want!
    
    return {
        'message': '✅ My automation finished!',
        'data': {'items_processed': 5}
    }
```

### Step 2: Run it

```bash
python bot.py
```

## 🏗️ Complex Bots with Multiple Tasks

For larger automation projects, organize your code into subtasks:

### Create Task Modules

Create a `tasks/` folder and organize your subtasks:

```
openautomate-bot-template/
├── bot.py                     # Main orchestrator
├── tasks/                     # 👈 Your subtasks here
│   ├── __init__.py           # Makes it a Python package
│   ├── email_tasks.py        # Email automation
│   ├── file_tasks.py         # File processing
│   ├── web_tasks.py          # Web scraping
│   └── excel_tasks.py        # Excel automation
├── framework/                 # Bot utilities
└── config/                    # Configuration
```

### Example: Email Task Module

**`tasks/email_tasks.py`**:
```python
"""
Email automation tasks
"""
import smtplib
from email.mime.text import MimeText

def send_report(logger, smtp_config, recipient, report_data):
    """Send email report"""
    logger.info(f"📧 Sending report to {recipient}")
    
    # Create email
    msg = MimeText(f"Automation Report: {report_data}")
    msg['Subject'] = 'Daily Automation Report'
    msg['From'] = smtp_config['from_email']
    msg['To'] = recipient
    
    # Send email
    with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.send_message(msg)
    
    logger.info("✅ Email sent successfully")
    return True

def check_inbox(logger, imap_config):
    """Check for new emails"""
    logger.info("📬 Checking inbox...")
    # IMAP logic here
    return []
```

### Example: File Processing Tasks

**`tasks/file_tasks.py`**:
```python
"""
File processing tasks
"""
import shutil
from pathlib import Path

def process_csv_files(logger, input_folder, output_folder):
    """Process all CSV files"""
    logger.info("📊 Processing CSV files...")
    
    processed_count = 0
    for csv_file in Path(input_folder).glob("*.csv"):
        logger.info(f"Processing: {csv_file.name}")
        
        # Your CSV processing logic
        # Example: Convert, clean, transform data
        
        # Save to output
        output_file = Path(output_folder) / f"processed_{csv_file.name}"
        shutil.copy2(csv_file, output_file)
        processed_count += 1
    
    logger.info(f"✅ Processed {processed_count} CSV files")
    return processed_count

def organize_files(logger, source_folder):
    """Organize files by type"""
    logger.info("🗂️ Organizing files by type...")
    
    file_types = {
        'images': ['.jpg', '.png', '.gif'],
        'documents': ['.pdf', '.docx', '.txt'],
        'spreadsheets': ['.xlsx', '.csv']
    }
    
    organized_count = 0
    for file_path in Path(source_folder).iterdir():
        if file_path.is_file():
            # Move to appropriate subfolder
            for folder_name, extensions in file_types.items():
                if file_path.suffix.lower() in extensions:
                    dest_folder = Path(source_folder) / folder_name
                    dest_folder.mkdir(exist_ok=True)
                    shutil.move(str(file_path), dest_folder / file_path.name)
                    organized_count += 1
                    break
    
    logger.info(f"✅ Organized {organized_count} files")
    return organized_count
```

### Example: Main Bot Orchestration

**`bot.py`** (updated for complex workflows):
```python
"""
Complex Bot Example - Orchestrates multiple tasks
"""
import sys
import os
from pathlib import Path

# Add framework and tasks to path
framework_path = os.path.join(os.path.dirname(__file__), 'framework')
sys.path.insert(0, framework_path)
sys.path.insert(0, os.path.dirname(__file__))  # For tasks

from base_bot import BaseBot
from transaction_folders import create_transaction_folders, ensure_folder

# Import your task modules
try:
    from tasks import email_tasks, file_tasks, web_tasks
except ImportError as e:
    print(f"⚠️  Some task modules not found: {e}")
    print("Create them in the tasks/ folder as needed")

class ComplexBot(BaseBot):
    """
    Complex automation bot that orchestrates multiple tasks
    """
    
    def execute(self):
        """
        Main workflow - orchestrate all subtasks
        """
        self.logger.info("🤖 Starting complex automation workflow...")
        
        # Create working folders
        create_transaction_folders(self.bot_name, self.logger)
        input_folder = ensure_folder(self.bot_name, "input")
        output_folder = ensure_folder(self.bot_name, "output")
        
        results = {
            'message': '✅ Complex automation completed!',
            'data': {
                'tasks_completed': [],
                'files_processed': 0,
                'emails_sent': 0,
                'errors': []
            }
        }
        
        try:
            # Task 1: Process files
            self.update_status("Processing files...")
            files_processed = self._process_files(input_folder, output_folder)
            results['data']['files_processed'] = files_processed
            results['data']['tasks_completed'].append('file_processing')
            
            # Task 2: Web scraping (if needed)
            self.update_status("Gathering web data...")
            web_data = self._scrape_data()
            if web_data:
                results['data']['tasks_completed'].append('web_scraping')
            
            # Task 3: Send reports
            self.update_status("Sending reports...")
            emails_sent = self._send_reports(results['data'])
            results['data']['emails_sent'] = emails_sent
            if emails_sent > 0:
                results['data']['tasks_completed'].append('email_reports')
            
            # Task 4: Cleanup
            self.update_status("Cleaning up...")
            self._cleanup_old_files()
            results['data']['tasks_completed'].append('cleanup')
            
        except Exception as e:
            self.logger.error(f"❌ Error in workflow: {e}")
            results['data']['errors'].append(str(e))
            raise
        
        self.logger.info("🎉 Complex automation workflow finished!")
        return results
    
    def _process_files(self, input_folder, output_folder):
        """Process files using file_tasks module"""
        try:
            return file_tasks.process_csv_files(self.logger, input_folder, output_folder)
        except Exception as e:
            self.logger.error(f"File processing failed: {e}")
            return 0
    
    def _scrape_data(self):
        """Scrape web data using web_tasks module"""
        try:
            # Get target URL from assets or config
            target_url = self.get_asset('scraper_url') or 'https://example.com'
            return web_tasks.scrape_website(self.logger, target_url)
        except Exception as e:
            self.logger.error(f"Web scraping failed: {e}")
            return None
    
    def _send_reports(self, report_data):
        """Send email reports using email_tasks module"""
        try:
            # Get email config from assets
            smtp_config = {
                'server': self.get_asset('smtp_server') or 'smtp.gmail.com',
                'port': 587,
                'username': self.get_asset('email_username'),
                'password': self.get_asset('email_password'),
                'from_email': self.get_asset('from_email')
            }
            
            recipients = self.get_asset('report_recipients') or 'admin@company.com'
            
            if smtp_config['username'] and smtp_config['password']:
                email_tasks.send_report(self.logger, smtp_config, recipients, report_data)
                return 1
            else:
                self.logger.info("📧 Email credentials not configured, skipping reports")
                return 0
                
        except Exception as e:
            self.logger.error(f"Email sending failed: {e}")
            return 0
    
    def _cleanup_old_files(self):
        """Clean up old files"""
        temp_folder = ensure_folder(self.bot_name, "temp")
        # Cleanup logic here
        self.logger.info("🧹 Cleanup completed")

# Run the complex bot
if __name__ == "__main__":
    print("🚀 Starting Complex Automation Bot...")
    
    # Load config to get bot name
    try:
        from config_manager import ConfigManager
        config_manager = ConfigManager()
        bot_name = config_manager.get('bot.name', 'ComplexBot')
        print(f"📋 Using bot name from config: {bot_name}")
    except Exception as e:
        print(f"⚠️  Could not load config, using default name: {e}")
        bot_name = 'ComplexBot'
    
    # Create and run complex bot
    bot = ComplexBot(bot_name)
    results = bot.run()
    
    # Print detailed results
    if results['success']:
        print(f"✅ SUCCESS: {results['message']}")
        print(f"📊 Tasks completed: {', '.join(results['data']['tasks_completed'])}")
        print(f"📁 Files processed: {results['data']['files_processed']}")
        print(f"📧 Emails sent: {results['data']['emails_sent']}")
        print(f"⏱️  Completed in {results['execution_time']:.2f} seconds")
    else:
        print(f"❌ FAILED: {results['message']}")
        if results['data']['errors']:
            print(f"❌ Errors: {', '.join(results['data']['errors'])}")
    
    print("👋 Complex bot finished!")
```

### Create Tasks Package

**`tasks/__init__.py`**:
```python
"""
Automation Tasks Package

Organize your complex automation logic into focused modules.
"""

# You can import common utilities here if needed
from pathlib import Path

def get_task_folder():
    """Get the tasks folder path"""
    return Path(__file__).parent
```

## 📚 What You Get

### 🗂️ Automatic Folders
The bot creates folders for your files in `Documents/openautomate-bot/YourBot/`:
- `input/` - Put files to process here
- `output/` - Bot saves results here
- `temp/` - Temporary files
- `screenshots/` - Screenshots

### 🔑 Secure Assets
Get sensitive data safely:
```python
api_key = self.get_asset('api_key')        # Get API key
password = self.get_asset('database_pass')  # Get password
all_keys = self.get_all_asset_keys()       # See what's available
```

### 📝 Easy Logging
```python
self.logger.info("Starting task...")       # Info message
self.logger.warning("Something's odd...")   # Warning
self.logger.error("Oops, failed!")        # Error
```

### 📊 Status Updates
```python
self.update_status("Processing files...")   # Update progress
self.update_status("Almost done...")        # Keep users informed
```

## 🎯 Examples

### Basic File Processor
```python
def execute(self):
    # Get input folder
    input_folder = ensure_folder(self.bot_name, "input")
    output_folder = ensure_folder(self.bot_name, "output")
    
    # Process all text files
    for file in input_folder.glob("*.txt"):
        with open(file, 'r') as f:
            content = f.read()
        
        # Do something with content
        processed = content.upper()
        
        # Save result
        output_file = output_folder / f"processed_{file.name}"
        with open(output_file, 'w') as f:
            f.write(processed)
    
    return {'message': 'Files processed!'}
```

### Web Scraper
See `examples/simple_web_scraper.py` for a complete example!

### Asset Demo  
See `examples/asset_demo.py` to learn about secure data!

## 🛠️ Installation

### Core Requirements
```bash
pip install requests psutil
```

### For Web Scraping
```bash
pip install beautifulsoup4
```

### For Excel Automation
```bash
pip install openpyxl pandas
```

## 🔧 Configuration

Edit `config/config.ini` if needed:

```ini
[bot]
name = {{ cookiecutter.bot_name }}
description = {{ cookiecutter.bot_description }}
version = 1.0.0

[agent]
enabled = true
host = localhost
port = 8081

[logging]
level = INFO
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s

[folders]
base_path = Documents/openautomate-bot
create_subfolders = true
subfolder_names = input,output,temp,screenshots,logs
```

## 💡 Tips

1. **Start Simple** - Begin with logging and folder creation
2. **Use Examples** - Copy from the examples folder
3. **Test Often** - Run `python bot.py` frequently
4. **Check Folders** - Look in `Documents/openautomate-bot/YourBot/`
5. **Use Assets** - Store passwords and API keys as assets
6. **Organize Tasks** - For complex bots, create a `tasks/` folder
7. **Test Modules** - Test each task module independently

## 🆘 Need Help?

1. **Check Examples** - Look in `examples/` folder
2. **Read Logs** - The bot tells you what's happening
3. **Start Simple** - Just make it log "Hello World" first
4. **Ask for Help** - Contact the OpenAutomate team

## 🚀 Common Automation Ideas

- **File Processing** - Convert, rename, organize files
- **Web Scraping** - Extract data from websites  
- **Excel Automation** - Process spreadsheets
- **Email Tasks** - Send reports, check inbox
- **Database Work** - Import/export data
- **API Integration** - Connect to web services
- **Report Generation** - Create PDFs, charts
- **System Monitoring** - Check disk space, processes

## 🎉 You're Ready!

Just edit `bot.py` and run `python bot.py`. It's that simple!

Happy automating! 🤖