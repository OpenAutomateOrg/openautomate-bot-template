"""
Example: Asset Demo

Shows how to access assets from the OpenAutomate platform.
Assets are secure data like API keys, passwords, etc.
"""

import sys
import os

# Add framework to path
framework_path = os.path.join(os.path.dirname(__file__), '..', 'framework')
sys.path.insert(0, framework_path)

from base_bot import BaseBot
from transaction_folders import ensure_folder


class AssetDemoBot(BaseBot):
    """
    Demo bot that shows how to work with assets.
    """
    
    def execute(self):
        """
        Show how to get and use assets.
        """
        self.logger.info("Starting asset demo...")

        # Get all available asset keys
        asset_keys = self.get_all_asset_keys()
        self.logger.info(f"Found {len(asset_keys)} assets: {asset_keys}")

        # Try to get some common assets
        api_key = self.get_asset('api_key')
        database_url = self.get_asset('database_url')
        username = self.get_asset('username')

        # Show what we found (don't log actual values for security)
        found_assets = []
        if api_key:
            found_assets.append('api_key')
            self.logger.info("Found API key")

        if database_url:
            found_assets.append('database_url')
            self.logger.info("Found database URL")

        if username:
            found_assets.append('username')
            self.logger.info("Found username")
        
        # Save a summary file
        output_folder = ensure_folder(self.bot_name, "output")
        output_file = output_folder / "asset_summary.txt"
        
        with open(output_file, 'w') as f:
            f.write("Asset Demo Results\n")
            f.write("==================\n\n")
            f.write(f"Total assets available: {len(asset_keys)}\n")
            f.write(f"Assets we tried to get: api_key, database_url, username\n")
            f.write(f"Assets found: {', '.join(found_assets) if found_assets else 'None'}\n\n")
            
            f.write("All available asset keys:\n")
            for key in asset_keys:
                f.write(f"  - {key}\n")
            
            if not asset_keys:
                f.write("  (No assets configured)\n")
        
        self.logger.info(f"Summary saved to: {output_file}")

        return {
            'message': f'Asset demo completed! Found {len(asset_keys)} assets',
            'data': {
                'total_assets': len(asset_keys),
                'asset_keys': asset_keys,
                'found_assets': found_assets,
                'output_file': str(output_file)
            }
        }


if __name__ == "__main__":
    print("Starting Asset Demo Bot...")

    bot = AssetDemoBot("AssetDemoBot")
    results = bot.run()

    if results['success']:
        print(f"SUCCESS: {results['message']}")
        if results['data']['asset_keys']:
            print(f"Available assets: {', '.join(results['data']['asset_keys'])}")
        else:
            print("No assets configured (this is normal for standalone testing)")
    else:
        print(f"FAILED: {results['message']}")