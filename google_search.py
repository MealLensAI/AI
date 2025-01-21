from googlesearch import search  # Importing the search function from googlesearch-python
import ssl
import certifi

class GoogleSearch:
    def __init__(self, max_results=5):
        """
        Initialize GoogleSearch instance with maximum results.

        Args:
            max_results (int): Maximum number of results to return
        """
        self.max_results = max_results

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
                results.append({
                    'title': url,  # The title can be fetched separately if needed
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


