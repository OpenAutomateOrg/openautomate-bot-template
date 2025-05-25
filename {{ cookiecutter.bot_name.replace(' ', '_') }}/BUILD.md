# Bot Build Instructions

## Overview

This bot template includes an automated build system that creates deployment-ready packages for OpenAutomate.

## Build Process

### 1. Edit Bot Metadata

Edit `bot.json` to update your bot information:

```json
{
  "name": "My Awesome Bot",
  "description": "This bot automates awesome tasks",
  "version": "1.0.0"
}
```

**Important**: Only edit the `name` and `description` fields manually. The `version` field is automatically incremented during build.

### 2. Run Build Script

Simply double-click `build.bat` or run it from command line:

```cmd
build.bat
```

### 3. What Happens During Build

1. **Version Auto-Increment**: The patch version is automatically incremented (e.g., 1.0.0 → 1.0.1)
2. **Metadata Sync**: Bot metadata is synced from `bot.json` to `config/config.ini`
3. **Package Creation**: A ZIP file is created with the naming convention: `{bot_name}.{version}.zip`
4. **File Inclusion**: All necessary files are included:
   - `*.py` files (including `bot.py`)
   - `bot.json` and `requirements.txt`
   - `config/` directory
   - `framework/` directory
   - `examples/` and `tasks/` directories
   - Documentation files

### 4. Upload to OpenAutomate

After successful build, you'll get a ZIP file like `My_Awesome_Bot.1.0.1.zip` that you can upload directly to OpenAutomate.

## File Structure

```
your-bot/
├── bot.py              # Main bot file
├── bot.json           # Bot metadata (edit this)
├── build.bat          # Build script
├── sync-metadata.ps1  # Metadata sync script
├── requirements.txt   # Python dependencies
├── config/
│   └── config.ini     # Bot configuration (auto-updated)
├── framework/         # Bot framework files
├── examples/          # Example files
└── tasks/             # Task definitions
```

## Version Management

- **Manual**: Edit `bot.json` to set major/minor versions (e.g., 1.0.0 → 2.0.0)
- **Automatic**: Patch version increments automatically on each build (e.g., 1.0.0 → 1.0.1)

## Duplicate Prevention

The OpenAutomate backend will reject uploads if a package with the same name and version already exists. Make sure to:

1. Use unique bot names
2. Let the build system auto-increment versions
3. Manually increment major/minor versions for significant changes

## Troubleshooting

### Build Fails
- Ensure you're running from the bot directory
- Check that `bot.json` exists and is valid JSON
- Verify PowerShell execution policy allows scripts

### Upload Rejected
- Check if the package name and version combination already exists
- Increment the version in `bot.json` manually if needed
- Ensure the ZIP file contains a valid `bot.py` file

## CI/CD Integration (Future)

This build system is designed to work with CI/CD pipelines. The build script can be called from:
- GitHub Actions
- Azure DevOps
- Jenkins
- Any CI/CD system that supports Windows batch scripts 