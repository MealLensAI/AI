from duckduckgo_search import DDGS
import requests
import re
import time
from random import uniform
from fake_useragent import UserAgent
import logging
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoogleSearch:
    def __init__(self, max_results=5, max_retries=5):
        """
        Initialize WebSearch instance with maximum results and retries.

        Args:
            max_results (int): Maximum number of results to return
            max_retries (int): Maximum number of retries for failed requests
        """
        self.max_results = max_results
        self.max_retries = max_retries
        self.ua = UserAgent()
        self.session = requests.Session()
        self.ddgs = DDGS()
        self.visited_urls = set()  # Keep track of URLs we've already tried

    def clean_url(self, url):
        """Clean and normalize URL."""
        try:
            parsed = urlparse(url)
            return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        except:
            return url

    def get_page_info(self, url, retry_count=0):
        """
        Fetch the title and description of a webpage given its URL with retry logic.

        Args:
            url (str): The URL of the webpage
            retry_count (int): Current retry attempt number

        Returns:
            dict: A dictionary containing the title and description of the webpage
        """
        clean_url = self.clean_url(url)
        if clean_url in self.visited_urls:
            return None
        self.visited_urls.add(clean_url)

        try:
            # Add random delay between requests
            time.sleep(uniform(1, 2))
            
            headers = {
                'User-Agent': self.ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            response = self.session.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            # Try multiple patterns for title
            title = None
            title_patterns = [
                r'<title>(.*?)</title>',
                r'<meta property="og:title" content="(.*?)"',
                r'<h1[^>]*>(.*?)</h1>'
            ]
            
            for pattern in title_patterns:
                title_match = re.search(pattern, response.text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    if title:
                        break

            # Try multiple patterns for description
            description = None
            desc_patterns = [
                r'<meta name="description" content="(.*?)"',
                r'<meta property="og:description" content="(.*?)"',
                r'<meta name="twitter:description" content="(.*?)"'
            ]
            
            for pattern in desc_patterns:
                desc_match = re.search(pattern, response.text, re.IGNORECASE)
                if desc_match:
                    description = desc_match.group(1).strip()
                    if description:
                        break

            # If we don't have both title and description, try to extract from content
            if not description:
                # Try to get first paragraph as description
                p_match = re.search(r'<p[^>]*>(.*?)</p>', response.text, re.IGNORECASE)
                if p_match:
                    description = p_match.group(1).strip()
                    # Clean HTML tags from description
                    description = re.sub(r'<[^>]+>', '', description)
                    description = description[:200] + '...' if len(description) > 200 else description

            # If still missing information and haven't exceeded retries, try again
            if (not title or not description) and retry_count < self.max_retries:
                logger.info(f"Retrying {url} (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(uniform(2, 4))  # Longer delay between retries
                return self.get_page_info(url, retry_count + 1)

            return {
                'title': title or 'No title found',
                'description': description or 'No description found'
            }

        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {str(e)}")
            if retry_count < self.max_retries:
                time.sleep(uniform(2, 4))
                return self.get_page_info(url, retry_count + 1)
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {url}: {str(e)}")
            if retry_count < self.max_retries:
                time.sleep(uniform(2, 4))
                return self.get_page_info(url, retry_count + 1)
            return None

    def get_search_results(self, query):
        """
        Get search results based on a query using DuckDuckGo with fallback handling.

        Args:
            query (str): The search term to find results for

        Returns:
            list: List of dictionaries containing result titles, descriptions, and URLs
        """
        try:
            results = []
            search_attempts = 0
            max_search_attempts = 3  # Increased number of search attempts
            
            while search_attempts < max_search_attempts and len(results) < self.max_results:
                # Modify query for subsequent attempts
                if search_attempts > 0:
                    query_modifiers = [
                        "detailed information guide tutorial",
                        "complete guide how to",
                        "full tutorial step by step"
                    ]
                    query = f"{query} {query_modifiers[search_attempts - 1]}"
                
                # Use DuckDuckGo search
                search_results = list(self.ddgs.text(
                    query,
                    max_results=self.max_results * 3,  # Get more results for fallback
                    region='wt-wt',
                    safesearch='moderate'
                ))

                for result in search_results:
                    try:
                        url = result.get('href', '')
                        if not url:
                            continue

                        # Get page info
                        page_info = self.get_page_info(url)
                        
                        # Skip if we couldn't get page info
                        if not page_info:
                            continue
                        
                        # Skip results with missing information
                        if page_info['title'] == 'No title found' or page_info['description'] == 'No description found':
                            continue
                        
                        # Use DuckDuckGo's title and description as fallback
                        title = page_info['title'] or result.get('title', '')
                        description = page_info['description'] or result.get('body', '')
                        
                        # Only add if we have both title and description
                        if title and description:
                            results.append({
                                'title': title,
                                'description': description,
                                'link': url
                            })

                            # If we have enough good results, return them
                            if len(results) >= self.max_results:
                                return results[:self.max_results]

                    except Exception as e:
                        logger.error(f"Error processing result: {str(e)}")
                        continue

                search_attempts += 1
                time.sleep(uniform(2, 4))  # Delay between search attempts

            # Return what we have, even if less than max_results
            return results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def main(self, query):
        """
        Main method to handle user input and output search results.
        """
        try:
            results = self.get_search_results(query)
            return results
        except Exception as e:
            logger.error(f"Main method error: {str(e)}")
            return []


if __name__ == "__main__":
    try:
        web_search = GoogleSearch(max_results=5)
        query = input("Enter your search query: ")
        results = web_search.main(query)

        if results:
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Description: {result['description']}")
                print(f"   Link: {result['link']}")
        else:
            print("No results found or an error occurred.")
    except KeyboardInterrupt:
        print("\nSearch interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")