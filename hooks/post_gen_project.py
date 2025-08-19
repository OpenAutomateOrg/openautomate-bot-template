#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Post-generation hook for OpenAutomate bot template.
Displays success message with bot details after project generation.
"""

import os
import sys

def main():
    """Display success message with bot information."""
    
    # Ensure UTF-8 encoding for output
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass
    
    # Get bot information from cookiecutter variables
    bot_name = "{{ cookiecutter.bot_name }}"
    bot_description = "{{ cookiecutter.bot_description }}"
    version = "1.0.0"  # Default version, not prompted to user
    
    # Get the current directory (generated project directory)
    project_dir = os.path.basename(os.getcwd())
    
    # Display success message (using ASCII-safe characters for Windows compatibility)
    print("\n" + "="*60)
    print("SUCCESS: Bot Template Generated Successfully!")
    print("="*60)
    print(f"Bot Name: {bot_name}")
    print(f"Description: {bot_description}")
    print(f"Version: {version}")
    print(f"Project Directory: {project_dir}")
    print("="*60)
    print("\nNext Steps:")
    print(f"   1. cd {project_dir}")
    print("   2. pip install -r requirements.txt")
    print("   3. Edit bot.py to add your automation logic")
    print("   4. python bot.py")
    print("\nTips:")
    print("   - Check the examples/ folder for inspiration!")
    print("   - Read BUILD.md for detailed setup instructions.")
    print("\nHappy automating!")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()