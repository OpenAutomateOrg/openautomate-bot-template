"""
Web Scraping Tasks

Handle web scraping, API calls, and web automation.
"""

from pathlib import Path
from . import log_task_start, log_task_complete, log_task_error

# Optional dependencies - will gracefully fail if not installed
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from bs4 import BeautifulSoup
    HAS_BEAUTIFULSOUP = True
except ImportError:
    HAS_BEAUTIFULSOUP = False


def scrape_website(logger, url, output_folder=None):
    """
    Scrape basic information from a website.
    
    Args:
        logger: Logger instance
        url: URL to scrape
        output_folder: Optional folder to save results
        
    Returns:
        dict: Scraped data
    """
    log_task_start(logger, "Web Scraping")
    
    if not HAS_REQUESTS:
        error_msg = "requests library not installed. Run: pip install requests"
        log_task_error(logger, "Web Scraping", error_msg)
        raise ImportError(error_msg)
    
    if not HAS_BEAUTIFULSOUP:
        error_msg = "beautifulsoup4 library not installed. Run: pip install beautifulsoup4"
        log_task_error(logger, "Web Scraping", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"🌐 Scraping: {url}")
        
        # Make request with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # Parse HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic information
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else "No title found"
        
        # Get all links (limit to first 20)
        links = []
        for link in soup.find_all('a', href=True)[:20]:
            link_text = link.get_text(strip=True)
            if link_text:  # Only include links with text
                links.append({
                    'text': link_text,
                    'url': link['href']
                })
        
        # Get all headings
        headings = []
        for i in range(1, 4):  # h1, h2, h3
            for heading in soup.find_all(f'h{i}'):
                heading_text = heading.get_text(strip=True)
                if heading_text:
                    headings.append({
                        'level': i,
                        'text': heading_text
                    })
        
        # Get meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', '') if meta_desc else ''
        
        scraped_data = {
            'url': url,
            'title': title_text,
            'description': description,
            'headings': headings,
            'links': links,
            'stats': {
                'total_headings': len(headings),
                'total_links': len(links)
            }
        }
        
        # Save to file if output folder specified
        if output_folder:
            save_scraped_data(logger, scraped_data, output_folder)
        
        log_task_complete(logger, "Web Scraping", f"Scraped {len(headings)} headings and {len(links)} links")
        return scraped_data
        
    except Exception as e:
        log_task_error(logger, "Web Scraping", str(e))
        raise


def save_scraped_data(logger, data, output_folder):
    """
    Save scraped data to a file.
    
    Args:
        logger: Logger instance
        data: Scraped data dictionary
        output_folder: Folder to save the file
    """
    try:
        import json
        from datetime import datetime
        
        output_path = Path(output_folder)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"scraped_data_{timestamp}.json"
        file_path = output_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Scraped data saved to: {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to save scraped data: {e}")


def check_website_status(logger, urls):
    """
    Check the status of multiple websites.
    
    Args:
        logger: Logger instance
        urls: List of URLs to check
        
    Returns:
        dict: Status results for each URL
    """
    log_task_start(logger, "Website Status Check")
    
    if not HAS_REQUESTS:
        error_msg = "requests library not installed. Run: pip install requests"
        log_task_error(logger, "Website Status Check", error_msg)
        raise ImportError(error_msg)
    
    try:
        results = {}
        
        for url in urls:
            logger.info(f"🔍 Checking: {url}")
            
            try:
                response = requests.get(url, timeout=10)
                results[url] = {
                    'status_code': response.status_code,
                    'status': 'online' if response.status_code == 200 else 'issues',
                    'response_time': response.elapsed.total_seconds()
                }
                
                if response.status_code == 200:
                    logger.info(f"✅ {url} is online ({response.elapsed.total_seconds():.2f}s)")
                else:
                    logger.warning(f"⚠️ {url} returned status {response.status_code}")
                    
            except Exception as e:
                results[url] = {
                    'status_code': None,
                    'status': 'offline',
                    'error': str(e)
                }
                logger.error(f"❌ {url} is offline: {e}")
        
        online_count = sum(1 for r in results.values() if r['status'] == 'online')
        log_task_complete(logger, "Website Status Check", f"{online_count}/{len(urls)} sites online")
        
        return results
        
    except Exception as e:
        log_task_error(logger, "Website Status Check", str(e))
        raise


def download_file(logger, url, output_folder, filename=None):
    """
    Download a file from a URL.
    
    Args:
        logger: Logger instance
        url: URL of the file to download
        output_folder: Folder to save the file
        filename: Optional custom filename
        
    Returns:
        str: Path to downloaded file
    """
    log_task_start(logger, "File Download")
    
    if not HAS_REQUESTS:
        error_msg = "requests library not installed. Run: pip install requests"
        log_task_error(logger, "File Download", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"⬇️ Downloading: {url}")
        
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Determine filename
        if not filename:
            filename = url.split('/')[-1]
            if not filename or '.' not in filename:
                filename = 'downloaded_file'
        
        output_path = Path(output_folder)
        file_path = output_path / filename
        
        # Download file in chunks
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        file_size = file_path.stat().st_size
        logger.info(f"💾 Downloaded {filename} ({file_size:,} bytes)")
        
        log_task_complete(logger, "File Download", f"Downloaded {filename}")
        return str(file_path)
        
    except Exception as e:
        log_task_error(logger, "File Download", str(e))
        raise


def make_api_request(logger, url, method='GET', headers=None, data=None):
    """
    Make an API request.
    
    Args:
        logger: Logger instance
        url: API endpoint URL
        method: HTTP method (GET, POST, etc.)
        headers: Optional headers dictionary
        data: Optional data for POST requests
        
    Returns:
        dict: API response data
    """
    log_task_start(logger, "API Request")
    
    if not HAS_REQUESTS:
        error_msg = "requests library not installed. Run: pip install requests"
        log_task_error(logger, "API Request", error_msg)
        raise ImportError(error_msg)
    
    try:
        logger.info(f"🔗 Making {method} request to: {url}")
        
        # Default headers
        if headers is None:
            headers = {'Content-Type': 'application/json'}
        
        # Make request
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            response = requests.request(method, url, headers=headers, json=data, timeout=30)
        
        response.raise_for_status()
        
        # Try to parse JSON response
        try:
            result = response.json()
        except:
            result = {'text': response.text, 'status_code': response.status_code}
        
        logger.info(f"✅ API request successful (status: {response.status_code})")
        log_task_complete(logger, "API Request", f"Status {response.status_code}")
        
        return result
        
    except Exception as e:
        log_task_error(logger, "API Request", str(e))
        raise 