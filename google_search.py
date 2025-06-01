from googlesearch import search  # Importing the search function from googlesearch-python
import ssl
import certifi
import requests
import re
import time
from random import uniform
from urllib.parse import urlparse


class GoogleSearch:
    def __init__(self, max_results=5):
        """
        Initialize GoogleSearch instance with maximum results.

        Args:
            max_results (int): Maximum number of results to return
        """
        self.max_results = max_results
        self.visited_urls = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        })

    def is_valid_url(self, url):
        """Check if the URL is valid and not an image or other media file."""
        try:
            parsed = urlparse(url)
            # Skip image URLs and other media files
            if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx']):
                return False
            # Skip URLs without a proper domain
            if not parsed.netloc or len(parsed.netloc.split('.')) < 2:
                return False
            return True
        except:
            return False

    def get_page_info(self, url, max_retries=3):
        """
        Fetch the title and description of a webpage given its URL.

        Args:
            url (str): The URL of the webpage
            max_retries (int): Maximum number of retries for failed requests

        Returns:
            dict: A dictionary containing the title and description of the webpage
        """
        if url in self.visited_urls:
            return None
        self.visited_urls.add(url)

        for attempt in range(max_retries):
            try:
                # Add delay between requests
                time.sleep(uniform(1, 2))

                response = self.session.get(url, timeout=10)
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

                # If we don't have a description, try to get it from content
                if not description:
                    # Try to get first paragraph as description
                    p_match = re.search(r'<p[^>]*>(.*?)</p>', response.text, re.IGNORECASE)
                    if p_match:
                        description = p_match.group(1).strip()
                        # Clean HTML tags from description
                        description = re.sub(r'<[^>]+>', '', description)
                        description = description[:200] + '...' if len(description) > 200 else description

                # Only return if we have both title and description
                if title and description and title != 'No title found' and description != 'No description found':
                    return {
                        'title': title,
                        'description': description
                    }

                # If we don't have valid results and haven't exceeded retries, try again
                if attempt < max_retries - 1:
                    time.sleep(uniform(2, 4))  # Longer delay between retries
                    continue

            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(uniform(2, 4))
                    continue
                print(f"Error fetching page info for {url}: {str(e)}")

        return None

    def get_search_results(self, query):
        """
        Get Google search results based on a query.

        Args:
            query (str): The search term to find results for

        Returns:
            list: List of dictionaries containing result titles, descriptions, and URLs
        """
        try:
            # Configure SSL context
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl._create_default_https_context = lambda: ssl_context

            results = []
            search_attempts = 0
            max_search_attempts = 5  # Increased number of search attempts

            while search_attempts < max_search_attempts and len(results) < self.max_results:
                try:
                    # Get more URLs than needed to account for invalid ones
                    urls = list(search(query, num_results=self.max_results * 2))

                    for url in urls:
                        if len(results) >= self.max_results:
                            break

                        if not self.is_valid_url(url):
                            continue

                        page_info = self.get_page_info(url)
                        if page_info:
                            results.append({
                                'title': page_info['title'],
                                'description': page_info['description'],
                                'link': url
                            })

                    # If we have enough results, return them
                    if len(results) >= self.max_results:
                        return results[:self.max_results]

                    # If we don't have enough results, modify the query and try again
                    search_attempts += 1
                    if search_attempts < max_search_attempts:
                        query_modifiers = [
                            "guide tutorial",
                            "how to",
                            "complete guide",
                            "detailed information"
                        ]
                        query = f"{query} {query_modifiers[search_attempts - 1]}"
                        time.sleep(uniform(2, 4))  # Delay between search attempts

                except Exception as e:
                    print(f"Search attempt {search_attempts + 1} failed: {str(e)}")
                    time.sleep(uniform(2, 4))
                    search_attempts += 1

            return results

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def main(self, query):
        """
        Main method to handle user input and output Google search results.
        """
        results = self.get_search_results(query)
        return results


if __name__ == "__main__":
    google_search = GoogleSearch(max_results=5)
    query = input("Enter your search query: ")
    results = google_search.main(query)

    if results:
        print("\nHere are your search results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Description: {result['description']}")
            print(f"   Link: {result['link']}")
    else:
        print("No results found or an error occurred.")


