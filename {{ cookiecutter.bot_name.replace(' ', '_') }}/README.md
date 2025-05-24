# {{cookiecutter.bot_name}}

{{cookiecutter.bot_description}}

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Edit your automation logic** in `bot.py` (look for the `execute()` method)

3. **Run your bot:**
   ```bash
   python bot.py
   ```

4. **Check results** in `Documents/openautomatebot/{{cookiecutter.bot_name}}/`

## 📁 Project Structure

```
{{cookiecutter.bot_name}}/
├── bot.py                    # 👈 Your main bot file - edit the execute() method!
├── framework/                # Bot framework (ready to use)
│   ├── base_bot.py          # Base bot class with OpenAutomate integration
│   ├── transaction_folders.py # Automatic folder management
│   └── logger_setup.py      # Professional logging setup
├── tasks/                    # Ready-to-use automation tasks
│   ├── file_tasks.py        # File processing utilities
│   ├── web_tasks.py         # Web scraping and API utilities
│   └── email_tasks.py       # Email automation utilities
├── examples/                 # Working examples
│   ├── simple_web_scraper.py # Web scraping example
│   ├── asset_demo.py        # Platform integration example
│   └── complex_bot_example.py # Advanced automation example
├── config/                   # Configuration files
│   └── config.ini           # Bot configuration
├── requirements.txt          # Dependencies
├── README.md                # This file
└── .gitignore               # Git ignore
```

## 📝 How to Use

### 1. Edit the `execute()` method in `bot.py`:

```python
def execute(self):
    # Add your automation logic here!
    
    # Get secure data from OpenAutomate platform
    api_key = self.get_asset('my_api_key')
    
    # Use ready-made tasks
    from tasks.file_tasks import process_csv_files
    from tasks.web_tasks import scrape_website
    from tasks.email_tasks import send_notification
    
    # Process files from input folder
    results = process_csv_files(self.input_folder, self.output_folder)
    
    # Send notification
    send_notification("Automation completed!", results)
```

### 2. Use Built-in Framework Features:

- **Automatic folder creation** - `Documents/openautomatebot/{{cookiecutter.bot_name}}/`
- **Professional logging** - `self.logger.info('message')`
- **OpenAutomate integration** - `self.get_asset('key')`, `self.update_status('status')`
- **Error handling** - Automatic timing and error reporting
- **Configuration management** - `config/config.ini`

### 3. Ready-to-Use Tasks:

**File Processing (`tasks/file_tasks.py`):**
```python
from tasks.file_tasks import process_csv_files, read_excel_file, save_json_data
```

**Web Automation (`tasks/web_tasks.py`):**
```python
from tasks.web_tasks import scrape_website, make_api_request, download_file
```

**Email Automation (`tasks/email_tasks.py`):**
```python
from tasks.email_tasks import send_email, send_notification, send_report
```

### 4. Working Examples:

- **`examples/simple_web_scraper.py`** - Basic web scraping
- **`examples/asset_demo.py`** - Platform integration demo
- **`examples/complex_bot_example.py`** - Advanced automation patterns

## ⚙️ Configuration

Edit `config/config.ini` for bot settings:

```ini
[bot]
name = {{cookiecutter.bot_name}}
version = 1.0.0

[agent]
host = localhost
port = 8080

[logging]
level = INFO
```

## 🔧 OpenAutomate Integration

### Secure Asset Management
```python
# Get sensitive data securely from platform
api_key = self.get_asset('api_key')
database_url = self.get_asset('database_url')
email_password = self.get_asset('email_password')
```

### Real-time Status Updates
```python
self.update_status("Processing files...")
self.update_status("Sending emails...")
self.update_status("Completed successfully!")
```

### Professional Logging
```python
self.logger.info("Starting automation...")
self.logger.warning("File not found, skipping...")
self.logger.error("Failed to connect to API")
```

## 📦 Adding Dependencies

The template includes common automation libraries. Uncomment in `requirements.txt` as needed:

```bash
# Already included:
pip install requests beautifulsoup4 selenium openpyxl pandas pillow

# For additional libraries:
pip install your-library-name
```

## 🎯 Common Automation Patterns

### File Processing Bot
```python
def execute(self):
    from tasks.file_tasks import process_csv_files
    
    results = process_csv_files(
        input_folder=ensure_folder(self.bot_name, "input"),
        output_folder=ensure_folder(self.bot_name, "output")
    )
    return results
```

### Web Scraping Bot
```python
def execute(self):
    from tasks.web_tasks import scrape_website
    
    data = scrape_website("https://example.com")
    
    # Save results
    output_file = ensure_folder(self.bot_name, "output") / "scraped_data.json"
    with open(output_file, 'w') as f:
        json.dump(data, f)
```

### Email Automation Bot
```python
def execute(self):
    from tasks.email_tasks import send_report
    
    # Process data
    results = self.process_data()
    
    # Send email report
    send_report(
        to_email=self.get_asset('recipient_email'),
        subject="Daily Report",
        data=results
    )
```

## 🚀 Deployment

When ready to deploy to OpenAutomate:

1. **Test locally**: `python bot.py`
2. **Package your bot** with all dependencies
3. **Upload to OpenAutomate platform**
4. **Configure assets** for secure data (API keys, passwords, etc.)
5. **Schedule or trigger** your automation

## 🆘 Need Help?

1. **Check examples** - Look in `examples/` folder
2. **Use ready-made tasks** - Check `tasks/` folder  
3. **Review framework** - Check `framework/` folder
4. **Test often** - Run `python bot.py` frequently

## 🎉 What You Get

✅ **Complete infrastructure** - Framework, tasks, examples, config  
✅ **OpenAutomate integration** - Asset management, status updates, logging  
✅ **Ready-to-use utilities** - File processing, web scraping, email automation  
✅ **Working examples** - Learn from real automation patterns  
✅ **Professional setup** - Logging, error handling, folder management  
✅ **Simple development** - Just edit the `execute()` method!  

Happy automating! 🤖 