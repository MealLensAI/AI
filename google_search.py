from googlesearch import search  # Importing the search function from googlesearch-python
import ssl
import certifi
import requests
import re


class GoogleSearch:
    def __init__(self, max_results=5):
        """
        Initialize GoogleSearch instance with maximum results.

        Args:
            max_results (int): Maximum number of results to return
        """
        self.max_results = max_results

    def get_page_title(self, url):
        """
        Fetch the title of a webpage given its URL.

        Args:
            url (str): The URL of the webpage

        Returns:
            str: The title of the webpage
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an error for bad responses
            # Use regex to find the title tag
            title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
            title = title_match.group(1) if title_match else 'No title found'
            return title
        except Exception as e:
            print(f"An error occurred while fetching the title: {str(e)}")
            return 'Error fetching title'

    def get_search_results(self, query):
        """
        Get Google search results based on a query.

        Args:
            query (str): The search term to find results for

        Returns:
            list: List of dictionaries containing result titles and URLs
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

                title = self.get_page_title(url)  # Fetch the title for each URL
                results.append({
                    'title': title,
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
            print(f"   Link: {result['link']}")
    else:
        print("No results found or an error occurred.")


