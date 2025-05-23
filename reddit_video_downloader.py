from bs4 import BeautifulSoup
import datetime
import os
import praw
import requests
import time

import config

class RedditVideoDownloader:
    
    def __init__(self, max_retries=20, retry_delay=2):
        self.reddit = self._initialize_reddit_client()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def _initialize_reddit_client(self):
        # Initialize and return Reddit client
        return praw.Reddit(
            username=config.username,
            password=config.password,
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent='Finding streamable links'
        )
    
    def create_time_range(self, year, month, day, start_hour=6, end_hour=9):
        # Create start and end datetime objects for the specified date and time range
        start_time = datetime.datetime(year, month, day, start_hour, 0, 0)
        end_time = datetime.datetime(year, month, day, end_hour, 0, 0)
        return start_time, end_time
    
    def search_reddit_posts(self, subreddit_name, search_query, start_time, end_time):
        # Search for Reddit posts within the specified time range
        subreddit = self.reddit.subreddit(subreddit_name)
        matching_posts = []
        
        for highlight in subreddit.search(search_query, sort='new', syntax='lucene'):
            submission_time = datetime.datetime.fromtimestamp(highlight.created_utc)
            if start_time <= submission_time <= end_time:
                matching_posts.append(highlight)
        
        return matching_posts
    
    def fetch_url_with_retry(self, url):
        # Fetch URL with retry logic and backoff strategy
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }

        for retry in range(self.max_retries):
            try:
                response = requests.get(url, headers=headers)
                if response.ok:
                    # print('Request successful.')
                    return response
            except requests.RequestException as e:
                print(f'Request failed (attempt {retry + 1}/{self.max_retries}): {e}')
                if retry < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        print('Maximum retries exceeded. Unable to establish connection.')
        return None
    
    def extract_video_url(self, page_content):
        # Extract video download URL from HTML content
        try:
            soup = BeautifulSoup(page_content, 'html.parser')
            video_meta = soup.find('meta', property='og:video:url')
            if video_meta and 'content' in video_meta.attrs:
                return video_meta['content']
        except Exception as e:
            print(f'Error extracting video URL: {e}')
        return None
    
    def download_video(self, video_url, file_name, folder='highlights'):
        # Download video from URL to specified folder
        try:
            os.makedirs(folder, exist_ok=True)
            file_path = os.path.join(folder, file_name)
            
            response = requests.get(video_url)
            if response.ok:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f'Video downloaded successfully: {file_path}')
                return True
            else:
                print(f'Failed to download video. Status code: {response.status_code}')
        except Exception as e:
            print(f'Error downloading video: {e}')
        return False
    
    def process_highlight_post(self, post, index):
        # Process a single highlight post and download its video
        title = post.title.replace('[Highlight] ', '')
        print(f"Processing: {title}")
        print(f'URL: {post.url}')
        
        # Fetch the page content
        response = self.fetch_url_with_retry(post.url)
        if not response:
            return False
        
        # Extract video download URL
        video_url = self.extract_video_url(response.text)
        if not video_url:
            print('Could not extract video URL.')
            return False
        
        # print(f'Video URL: {video_url}')
        
        # Download the video
        file_name = f'{title}.mp4'
        return self.download_video(video_url, file_name)
    
    def download_highlights_for_date(self, year, month, day, start_hour=6, end_hour=9, subreddit_name='nba'):
        # Main method to download all highlights for a specific date and time range

        # Create time range
        start_time, end_time = self.create_time_range(year, month, day, start_hour, end_hour)
        
        # Search for posts
        search_query = "url:streamable.com AND title:'[Highlight]'"
        posts = self.search_reddit_posts(subreddit_name, search_query, start_time, end_time)[:2]
        
        print(f'Found {len(posts)} matching posts.')
        
        # Process each post
        successful_downloads = 0
        for index, post in enumerate(posts):
            if self.process_highlight_post(post, index):
                successful_downloads += 1
        
        print(f'Successfully downloaded {successful_downloads}/{len(posts)} videos.')


def main():
    # Main function to run the video downloader
    downloader = RedditVideoDownloader()
    
    # Download highlights from May 22, 2025, between 8am and 9am
    downloader.download_highlights_for_date(2025, 5, 22, 8, 9)


if __name__ == '__main__':
    main()
