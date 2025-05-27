from pytube import Search
import ssl
import certifi
import time
import logging
from random import uniform
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeSearch:
    def __init__(self, api_key, max_results=5, max_retries=5):
        """
        Initialize YouTubeSearch instance with API key and max results.

        Args:
            api_key (str): The API key to access YouTube API
            max_results (int): Maximum number of results to return
            max_retries (int): Maximum number of retries for failed requests
        """
        self.api_key = api_key
        self.max_results = max_results
        self.max_retries = max_retries
        self.visited_videos = set()  # Keep track of videos we've already tried

    def clean_video_id(self, video_id):
        """Clean and normalize video ID."""
        try:
            return video_id.strip()
        except:
            return video_id

    def get_video_info(self, video, retry_count=0):
        """
        Get video information with retry logic.

        Args:
            video: The video object from pytube
            retry_count (int): Current retry attempt number

        Returns:
            dict: Dictionary containing video information or None if failed
        """
        video_id = self.clean_video_id(video.video_id)
        if video_id in self.visited_videos:
            return None
        self.visited_videos.add(video_id)

        try:
            # Add random delay between requests
            time.sleep(uniform(1, 2))

            # Get video information
            title = video.title
            link = f'https://youtube.com/watch?v={video_id}'

            # If we don't have a title and haven't exceeded retries, try again
            if not title and retry_count < self.max_retries:
                logger.info(f"Retrying video {video_id} (attempt {retry_count + 1}/{self.max_retries})")
                time.sleep(uniform(2, 4))  # Longer delay between retries
                return self.get_video_info(video, retry_count + 1)

            return {
                'title': title,
                'link': link
            }

        except Exception as e:
            logger.error(f"Error getting video info for {video_id}: {str(e)}")
            if retry_count < self.max_retries:
                time.sleep(uniform(2, 4))
                return self.get_video_info(video, retry_count + 1)
            return None

    def get_video_links(self, search_query, max_results=5):
        """
        Get YouTube video links based on a search query with retry logic.

        Args:
            search_query (str): The search term to find videos for
            max_results (int): Maximum number of results to return

        Returns:
            list: List of dictionaries containing video titles and links
        """
        try:
            # Configure SSL context
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            ssl._create_default_https_context = lambda: ssl_context

            search_attempts = 0
            max_search_attempts = 3
            results = []

            while search_attempts < max_search_attempts and len(results) < max_results:
                try:
                    # Modify query for subsequent attempts
                    if search_attempts > 0:
                        query_modifiers = [
                            "tutorial guide",
                            "how to make",
                            "step by step"
                        ]
                        modified_query = f"{search_query} {query_modifiers[search_attempts - 1]}"
                    else:
                        modified_query = search_query

                    # Use pytube to search for videos
                    s = Search(modified_query)
                    videos = list(s.results)

                    for video in videos:
                        try:
                            video_info = self.get_video_info(video)
                            
                            # Skip if we couldn't get video info
                            if not video_info:
                                continue

                            # Only add if we have both title and link
                            if video_info['title'] and video_info['link']:
                                results.append(video_info)

                                # If we have enough good results, return them
                                if len(results) >= max_results:
                                    return results[:max_results]

                        except Exception as e:
                            logger.error(f"Error processing video: {str(e)}")
                            continue

                    search_attempts += 1
                    time.sleep(uniform(2, 4))  # Delay between search attempts

                except Exception as e:
                    logger.error(f"Search attempt {search_attempts + 1} failed: {str(e)}")
                    search_attempts += 1
                    time.sleep(uniform(2, 4))

            # Return what we have, even if less than max_results
            return results

        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return []

    def main(self, food, max_results=5):
        """
        Main method to handle user input and output YouTube search results.
        """
        try:
            results = self.get_video_links(food, max_results)
            return results
        except Exception as e:
            logger.error(f"Main method error: {str(e)}")
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
    print(youtube_search.main("how to make rice"))
