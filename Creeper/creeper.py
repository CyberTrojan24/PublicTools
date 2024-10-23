import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import Set, List, Optional

class Creeper:
    """
    A simple web crawler that can traverse websites and collect links
    """
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.visited_urls: Set[str] = set()
        self.headers = {
            'User-Agent': 'Creeper/0.1.0 (Educational Purpose)'
        }

    def crawl(self, max_pages: Optional[int] = None) -> List[str]:
        """
        Start crawling from the base URL
        
        Args:
            max_pages: Maximum number of pages to crawl (None for unlimited)
            
        Returns:
            List of discovered URLs
        """
        pages_to_visit = [self.base_url]
        pages_crawled = 0

        while pages_to_visit and (max_pages is None or pages_crawled < max_pages):
            current_url = pages_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue

            try:
                response = requests.get(current_url, headers=self.headers)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    self.visited_urls.add(current_url)
                    pages_crawled += 1
                    
                    # Find all links on the page
                    new_urls = self._extract_links(soup, current_url)
                    pages_to_visit.extend(url for url in new_urls 
                                        if url not in self.visited_urls)
                    
            except Exception as e:
                print(f"Error crawling {current_url}: {str(e)}")

        return list(self.visited_urls)

    def _extract_links(self, soup: BeautifulSoup, current_url: str) -> List[str]:
        """
        Extract all links from a page
        """
        links = []
        for anchor in soup.find_all('a'):
            href = anchor.get('href')
            if href:
                absolute_url = urljoin(current_url, href)
                if absolute_url.startswith(self.base_url):
                    links.append(absolute_url)
        return links
