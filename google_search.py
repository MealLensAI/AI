from googleapiclient.discovery import build


class GoogleSearch:
    def __init__(self, api_key, cx, max_results=5):
        """
        Initialize GoogleSearch instance with API key, Custom Search Engine ID, and max results.

        Args:
            api_key (str): The API key to access Google Custom Search API
            cx (str): The Custom Search Engine ID
            max_results (int): Maximum number of results to return
        """
        self.api_key = api_key
        self.cx = cx
        self.max_results = max_results

    def get_search_results(self, search_query):
        """
        Get top Google search results based on a search query.

        Args:
            search_query (str): The search term to find results for

        Returns:
            list: List of dictionaries containing result titles and links
        """
        try:
            # Create the Custom Search API client
            service = build('customsearch', 'v1', developerKey=self.api_key)

            # Execute the search
            search_response = service.cse().list(
                q=search_query,
                cx=self.cx,
                num=self.max_results,
                filter='0',  # Filter out duplicate results
                safe='high',
            ).execute()

            # Process the results
            results = []
            for item in search_response.get('items', []):
                title = item.get('title', 'No Title')
                link = item.get('link', 'No Link')
                snippet = item.get('snippet', 'No Description')
                results.append({
                    'title': title,
                    'link': link,
                    'description': snippet
                })

            return results

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def main(self,food):
        """
        Main method to handle user input and output Google search results.
        """

        results = self.get_search_results(food)

        if results:

            return results
            # print("\nHere are your Google search results:")
            # for i, result in enumerate(results, 1):
            #     print(f"\n{i}. {result['title']}")
            #     print(f"   Link: {result['link']}")
            #     print(f"   Description: {result['description']}")
        else:
            return  []
            # print("No results found or an error occurred.")


if __name__ == "__main__":
    # Replace with your own API key and Custom Search Engine ID
    api_key = 'AIzaSyDHvkvp4jGmkIHntqrZ2HQGWC3HGqGtt_4'
    cx = '13a96d83a84c64f2d'

    # Create GoogleSearch instance
    google_search = GoogleSearch(api_key, cx)

    # Run the main method of the GoogleSearch class
    print(google_search.main("rice"))


