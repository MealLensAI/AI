from googleapiclient.discovery import build
from pytube import Search  # New import for the updated search method
import ssl
import certifi


class YouTubeSearch:
    def __init__(self, api_key, max_results=5):
        """
        Initialize YouTubeSearch instance with API key and max results.

        Args:
            api_key (str): The API key to access YouTube API
            max_results (int): Maximum number of results to return
        """
        self.api_key = api_key
        self.max_results = max_results

    def get_video_links(self, search_query, max_results=5):
        """
        Get YouTube video links based on a search query.

        Args:
            search_query (str): The search term to find videos for

        Returns:
            list: List of dictionaries containing video titles and links
        """
        try:
            # Configure SSL context
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl._create_default_https_context = lambda: ssl_context  # Correctly set the default context

            # Use pytube to search for videos
            s = Search(search_query)
            videos = []
            for video in s.results[:max_results]:
                videos.append({
                    'title': video.title,
                    'link': f'https://youtube.com/watch?v={video.video_id}'
                })

            return videos

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def main(self,food,max_results = 5):
        """
        Main method to handle user input and output YouTube search results.
        """

        results = self.get_video_links(food,max_results)

        if results:
            return results
            # print("\nHere are your video links:")
            # for i, video in enumerate(results, 1):
            #     print(f"\n{i}. {video['title']}")
            #     print(f"   Link: {video['link']}")
        else:
            # print("No videos found or an error occurred.")
            return []


if __name__ == "__main__":
    # Replace with your own API key
    api_key = "AIzaSyCMV1RzXC62lSyDxqcqlky-p1UzHqH2XEw"
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    youtube_api_key = 'AIzaSyAzk-urSNH6VtvH8cZdJlKT0cIdJKV9SJA'
    google_search_api_key = 'AIzaSyDHvkvp4jGmkIHntqrZ2HQGWC3HGqGtt_4'
    youtube_api_key = youtube_api_key

    # Create YouTubeSearch instance
    youtube_search = YouTubeSearch(youtube_api_key)

    # Run the main method of the YouTubeSearch class
    print(youtube_search.main("math"))
