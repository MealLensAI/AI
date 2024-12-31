# Google Search and YouTube Video Search with Python

This repository contains Python scripts for interacting with Google's APIs to perform two types of searches:
1. **Google Search** – Retrieves top Google search results based on a user query.
2. **YouTube Video Search** – Retrieves YouTube video links based on a user query.

Both scripts utilize the Google Custom Search API and the YouTube Data API to fetch results.

## Requirements

To use these scripts, you need:
- A Google Cloud Platform account.
- API keys for the **Google Custom Search API** and **YouTube Data API**.

### Install Dependencies
You'll need the following Python libraries:
- `google-api-python-client`
- `urllib.parse`

You can install them using `pip`:

pip install google-api-python-client


## Setup

1. **Get Your API Keys**:
    - [Google Custom Search API](https://developers.google.com/custom-search/v1/overview) – For Google search results.
    - [YouTube Data API v3](https://developers.google.com/youtube/v3/getting-started) – For YouTube video results.
    
2. **Set Your API Keys**:
    - Replace the `API_KEY` and `CX` (Custom Search Engine ID) in both scripts with your own credentials.

---

## Scripts

### 1. Google Search Results

This script allows you to get the top Google search results for a query.

#### How It Works:

- **`GoogleSearch` class**: Initializes with the API key and Custom Search Engine ID, and contains methods to perform searches and display results.
- **`get_search_results()`**: Searches Google for the given query and retrieves the top results.
- **`main()`**: Prompts the user for a search query and displays the results.

#### Example Usage:

python google_search.py

You will be prompted to input a search term, and the script will return the top Google search results.

---

### 2. YouTube Video Search

This script fetches YouTube video links based on a search query.

#### How It Works:

- **`YouTubeSearch` class**: Initializes with the API key and allows searching YouTube for video links.
- **`get_video_links()`**: Searches YouTube for the given query and retrieves video links.
- **`main()`**: Prompts the user for a search query and displays the video links.

#### Example Usage:
```bash
python youtube_search.py
```
You will be prompted to input a search term, and the script will return the YouTube video links.

---

## Example Code for Google Search

```python
from googleapiclient.discovery import build

class GoogleSearch:
    def __init__(self, api_key, cx, max_results=5):
        self.api_key = api_key
        self.cx = cx
        self.max_results = max_results

    def get_search_results(self, search_query):
        try:
            service = build('customsearch', 'v1', developerKey=self.api_key)
            search_response = service.cse().list(
                q=search_query,
                cx=self.cx,
                num=self.max_results,
                filter='0',  
                safe='high',
            ).execute()

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

    def main(self):
        search_term = input("Enter what you want to search for: ")
        results = self.get_search_results(search_term)

        if results:
            print("\nHere are your Google search results:")
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['title']}")
                print(f"   Link: {result['link']}")
                print(f"   Description: {result['description']}")
        else:
            print("No results found or an error occurred.")
```

---

## Contribution

Feel free to fork this repository, make changes, and submit pull requests. Any improvements or bug fixes are welcome!

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

For issues or questions, please open an issue on the GitHub repository.

---

## Acknowledgments

- Google for providing powerful APIs like the Custom Search API and YouTube Data API.
- Python community for the `google-api-python-client` library, which makes API integration straightforward.
```