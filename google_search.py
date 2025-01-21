from googlesearch import search  # Importing the search function from googlesearch-python
import ssl
import certifi
import requests
from bs4 import BeautifulSoup

class GoogleSearch:
    def __init__(self, max_results=5):
        """
        Initialize GoogleSearch instance with maximum results.

        Args:
            max_results (int): Maximum number of results to return
        """
        self.max_results = max_results

    def get_page_info(self, url):
        """
        Fetch the title and description of a webpage given its URL.

        Args:
            url (str): The URL of the webpage

        Returns:
            dict: A dictionary containing the title and description of the webpage
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the title
            title = soup.title.string if soup.title else 'No title found'
            
            # Extract the meta description
            description = ''
            description_tag = soup.find('meta', attrs={'name': 'description'})
            if description_tag and 'content' in description_tag.attrs:
                description = description_tag['content']
            else:
                description = 'No description found'
            
            return {
                'title': title,
                'description': description
            }
        except Exception as e:
            print(f"An error occurred while fetching the title and description: {str(e)}")
            return {'title': 'Error fetching title', 'description': 'Error fetching description'}

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
            ssl._create_default_https_context = lambda: ssl_context  # Correctly set the default context

            results = []
            for url in search(query, num_results=self.max_results):
                # Ensure the URL is absolute
                if not url.startswith(('http://', 'https://')):
                    continue  # Skip invalid URLs

                page_info = self.get_page_info(url)  # Fetch the title and description for each URL
                results.append({
                    'title': page_info['title'],
                    'description': page_info['description'],
                    'link': url
                })

            return results

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def main(self, query):
        """
        Main method to handle user input and output Google search results.
        """
        results = self.get_search_results(query)

        if results:
            return results
        else:
            return []

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


