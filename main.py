
import ssl
import certifi
from pytube import Search
import time
import urllib.request


def search_youtube(query, max_results=5):
    """
    Search YouTube and return direct video links without using an API.

    Args:
        query (str): Search term
        max_results (int): Maximum number of results to return

    Returns:
        list: List of dictionaries containing video titles and URLs
    """
    try:
        # Configure SSL context
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        ssl._create_default_https_context = ssl._create_unverified_context

        # Create a Search object
        s = Search(query)

        # Get search results
        results = []
        for video in s.results[:max_results]:
            results.append({
                'title': video.title,
                'url': f'https://youtube.com/watch?v={video.video_id}'
            })

        return results

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []


def main():
    # First ensure we have certifi installed
    try:
        import certifi
    except ImportError:
        print("Installing required certifi package...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'certifi'])
        import certifi

    while True:
        # Get search query from user
        search_term = input("\nEnter what you want to search for (or 'quit' to exit): ")

        if search_term.lower() == 'quit':
            break

        print("\nSearching YouTube...")
        results = search_youtube(search_term)

        if results:
            print("\nHere are your video links:")
            for i, video in enumerate(results, 1):
                print(f"\n{i}. {video['title']}")
                print(f"   Link: {video['url']}")
        else:
            print("No videos found or an error occurred. Try another search term.")

        time.sleep(1)  # Small delay to prevent too many rapid searches


if __name__ == "__main__":
    print("YouTube Video Link Finder (No API required)")
    print("----------------------------------------")

    # Install required packages if not already installed
    try:
        import pytube
    except ImportError:
        print("Installing required packages...")
        import subprocess

        subprocess.check_call(['pip', 'install', 'pytube'])
        subprocess.check_call(['pip', 'install', 'certifi'])

    main()
