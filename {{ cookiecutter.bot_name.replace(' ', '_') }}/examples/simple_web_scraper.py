"""
Example: Simple Web Scraper

Shows how to create a bot that scrapes websites.
Just change the URL and run it!
"""

import sys
import os

# Add framework to path
framework_path = os.path.join(os.path.dirname(__file__), '..', 'framework')
sys.path.insert(0, framework_path)

from base_bot import BaseBot
from transaction_folders import ensure_folder

# Optional: Install with "pip install requests beautifulsoup4"
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Please install: pip install requests beautifulsoup4")
    sys.exit(1)


class WebScraperBot(BaseBot):
    """
    Simple web scraper bot.
    """
    
    def execute(self):
        """
        Scrape a website and save results.
        """
        self.logger.info("Starting web scraping...")

        # Get URL to scrape (try from assets first, then use default)
        url = self.get_asset('scraper_url') or 'https://httpbin.org/html'

        self.logger.info(f"Scraping: {url}")
        self.update_status(f"Scraping {url}")
        
        try:
            # Scrape the website
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data
            title = soup.find('title')
            title_text = title.get_text(strip=True) if title else "No title"
            
            # Get all links
            links = []
            for link in soup.find_all('a', href=True)[:10]:  # Limit to 10
                links.append({
                    'text': link.get_text(strip=True),
                    'url': link['href']
                })
            
            # Get all headings
            headings = []
            for i in range(1, 4):  # h1, h2, h3
                for heading in soup.find_all(f'h{i}'):
                    headings.append(heading.get_text(strip=True))
            
            # Save results to file
            output_folder = ensure_folder(self.bot_name, "output")
            output_file = output_folder / "scraped_data.txt"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Web Scraping Results\n")
                f.write(f"URL: {url}\n")
                f.write(f"Title: {title_text}\n\n")
                
                f.write("Headings:\n")
                for heading in headings:
                    f.write(f"  - {heading}\n")
                
                f.write(f"\nLinks ({len(links)}):\n")
                for link in links:
                    f.write(f"  - {link['text']}: {link['url']}\n")
            
            self.logger.info(f"Results saved to: {output_file}")

            return {
                'message': f'Successfully scraped {url}',
                'data': {
                    'url': url,
                    'title': title_text,
                    'headings_found': len(headings),
                    'links_found': len(links),
                    'output_file': str(output_file)
                }
            }

        except Exception as e:
            self.logger.error(f"Scraping failed: {e}")
            raise


if __name__ == "__main__":
    print("Starting Web Scraper Bot...")

    bot = WebScraperBot("WebScraperBot")
    results = bot.run()

    if results['success']:
        print(f"SUCCESS: {results['message']}")
        print(f"Found {results['data']['headings_found']} headings and {results['data']['links_found']} links")
    else:
        print(f"FAILED: {results['message']}")