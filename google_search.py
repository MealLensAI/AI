from googleapiclient.discovery import build


def get_google_search_results(search_query, max_results=5):
    """
    Get top Google search results based on a search query.

    Args:
        search_query (str): The search term to find results for
        max_results (int): Maximum number of search results to return

    Returns:
        list: List of dictionaries containing result titles and links
    """
    try:
        # Replace with your own Google API key and Custom Search Engine ID
        API_KEY = 'AIzaSyDHvkvp4jGmkIHntqrZ2HQGWC3HGqGtt_4'

        CX = '13a96d83a84c64f2d'

        # Create the Custom Search API client
        service = build('customsearch', 'v1', developerKey=API_KEY)

        # Execute the search
        search_response = service.cse().list(
            q=search_query,
            cx=CX,
            num=max_results,

            # sort='date',  # Sort results by date (optional, you can remove if not needed)
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


# Example usage
def main():
    search_term = input("Enter what you want to search for: ")
    results = get_google_search_results(search_term)

    if results:
        print("\nHere are your Google search results:")
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result['title']}")
            print(f"   Link: {result['link']}")
            print(f"   Description: {result['description']}")
    else:
        print("No results found or an error occurred.")


if __name__ == "__main__":
    main()
