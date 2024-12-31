

from googleapiclient.discovery import build
from urllib.parse import quote


def get_youtube_links(search_query, max_results=5):
    """
    Get direct YouTube video links based on a search query.

    Args:
        search_query (str): The search term to find videos for
        max_results (int): Maximum number of video links to return

    Returns:
        list: List of dictionaries containing video titles and links
    """
    try:
        # You'll need to replace this with your own API key
        API_KEY = 'AIzaSyCgbgyVCdZy4oBTw8UvL3_UmD6tVi0ovyw'

        # Create YouTube API client
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Call the search.list method to get search results
        search_response = youtube.search().list(
            q=search_query,
            part='id,snippet',
            maxResults=max_results,
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


# Example usage
def main():
    search_term = input("Enter what you want to search for: ")
    results = get_youtube_links(search_term)

    if results:
        print("\nHere are your video links:")
        for i, video in enumerate(results, 1):
            print(f"\n{i}. {video['title']}")
            print(f"   Link: {video['link']}")
    else:
        print("No videos found or an error occurred.")


if __name__ == "__main__":
    main()


# import ssl
# import certifi
# from pytube import Search
# import time
# import urllib.request
#
#
# def search_youtube(query, max_results=5):
#     """
#     Search YouTube and return direct video links without using an API.
#
#     Args:
#         query (str): Search term
#         max_results (int): Maximum number of results to return
#
#     Returns:
#         list: List of dictionaries containing video titles and URLs
#     """
#     try:
#         # Configure SSL context
#         ssl_context = ssl.create_default_context(cafile=certifi.where())
#         ssl._create_default_https_context = ssl._create_unverified_context
#
#         # Create a Search object
#         s = Search(query)
#
#         # Get search results
#         results = []
#         for video in s.results[:max_results]:
#             results.append({
#                 'title': video.title,
#                 'url': f'https://youtube.com/watch?v={video.video_id}'
#             })
#
#         return results
#
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return []
#
#
# def main():
#     # First ensure we have certifi installed
#     try:
#         import certifi
#     except ImportError:
#         print("Installing required certifi package...")
#         import subprocess
#         subprocess.check_call(['pip', 'install', 'certifi'])
#         import certifi
#
#     while True:
#         # Get search query from user
#         search_term = input("\nEnter what you want to search for (or 'quit' to exit): ")
#
#         if search_term.lower() == 'quit':
#             break
#
#         print("\nSearching YouTube...")
#         results = search_youtube(search_term)
#
#         if results:
#             print("\nHere are your video links:")
#             for i, video in enumerate(results, 1):
#                 print(f"\n{i}. {video['title']}")
#                 print(f"   Link: {video['url']}")
#         else:
#             print("No videos found or an error occurred. Try another search term.")
#
#         time.sleep(1)  # Small delay to prevent too many rapid searches
#
# AIzaSyCgbgyVCdZy4oBTw8UvL3_UmD6tVi0ovyw
# if __name__ == "__main__":
#     print("YouTube Video Link Finder (No API required)")
#     print("----------------------------------------")
#
#     # Install required packages if not already installed
#     try:
#         import pytube
#     except ImportError:
#         print("Installing required packages...")
#         import subprocess
#
#         subprocess.check_call(['pip', 'install', 'pytube'])
#         subprocess.check_call(['pip', 'install', 'certifi'])
#
#     main()
