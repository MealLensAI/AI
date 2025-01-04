from googleapiclient.discovery import build


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

    def get_video_links(self, search_query):
        """
        Get YouTube video links based on a search query.

        Args:
            search_query (str): The search term to find videos for

        Returns:
            list: List of dictionaries containing video titles and links
        """

        try:
            # Create YouTube API client
            youtube = build('youtube', 'v3', developerKey=self.api_key)

            # Call the search.list method to get search results
            search_response = youtube.search().list(
                q=search_query,
                part='id,snippet',
                maxResults=self.max_results,
                type='video'
            ).execute()

            # Process the results
            videos = []
            for search_result in search_response.get('items', []):
                if search_result['id']['kind'] == 'youtube#video':
                    video_id = search_result['id']['videoId']
                    title = search_result['snippet']['title']
                    link = f'https://www.youtube.com/watch?v={video_id}'
                    videos.append({
                        'title': title,
                        'link': link
                    })

            return videos

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return []

    def main(self,food):
        """
        Main method to handle user input and output YouTube search results.
        """

        results = self.get_video_links(food)

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
    api_key = 'AIzaSyCgbgyVCdZy4oBTw8UvL3_UmD6tVi0ovyw'

    # Create YouTubeSearch instance
    youtube_search = YouTubeSearch(api_key)

    # Run the main method of the YouTubeSearch class
    youtube_search.main()
