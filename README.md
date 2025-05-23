# Reddit Video Downloader

A Python script that automatically downloads videos from Reddit posts of  the given subreddit within a specified time range

Originally designed for obtaining NBA highlights from r/nba

## Demo

🎥 [Watch the demo](https://drive.google.com/file/d/1-Nd8fmrvVjWN6RXUpoQ2GVWlnqxJDJht/view?usp=sharing)

## Features

- Download videos from Reddit posts containing Streamable links
- Filter posts by specific date and time ranges
- Retry mechanism with exponential backoff for failed requests
- Modular, class-based design for easy customization
- Anti-bot protection bypass with realistic browser headers

## Prerequisites

- Python 3.8+
- [uv](https://docs.astral.sh/uv/) package manager
- Reddit account

## Installation

1. Clone this repository:
```bash
git clone https://github.com/deephelms28/Reddit-Video-Downloader.git
cd Reddit-Video-Downloader
```

2. Install required packages using uv:
```bash
uv add beautifulsoup4 praw requests
```

3. Set up Reddit API credentials (see Configuration section)

## Configuration

### Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App"
3. Fill out the form:
   - **Name**: Your app name (e.g., "Video Downloader")
   - **App type**: Select "script"
   - **Redirect URI**: `http://localhost:8080`
4. Click "Create app"

### Config File

Create a `config.py` file in the project directory:

```python
# Reddit API credentials
username = "your_reddit_username"
password = "your_reddit_password"
client_id = "your_client_id"
client_secret = "your_client_secret"
```

## Usage

### Basic Usage

```bash
uv run python reddit_video_downloader.py
```

Or in Python:

```python
from reddit_video_downloader import RedditVideoDownloader

# Initialize the downloader
downloader = RedditVideoDownloader()

# Download highlights from May 22, 2025, between 6am and 9am
downloader.download_highlights_for_date(2025, 5, 22, 6, 9)
```

### Custom Parameters

```python
# Custom retry settings
downloader = RedditVideoDownloader(max_retries=10, retry_delay=3)

# Different subreddit and time range
downloader.download_highlights_for_date(
    year=2024, 
    month=6, 
    day=15, 
    start_hour=8, 
    end_hour=12, 
    subreddit_name='soccer'
)
```

## How It Works

1. **Authentication**: Connects to Reddit API using your credentials
2. **Search**: Finds posts matching your criteria (Streamable links with "[Highlight]" in title)
3. **Filter**: Filters posts by specified date/time range
4. **Extract**: Scrapes Streamable pages to find direct video URLs
5. **Download**: Downloads videos with retry logic and anti-bot protection

## Customization

### Change Search Query

Modify the search query in `download_highlights_for_date()`

For example:

```python
search_query = 'url:streamable.com AND title:"[Highlight]"'
# Change to:
search_query = 'url:youtube.com AND flair:"Highlight"'
```

### Different Video Sources

The script can be adapted for other video hosting sites by modifying the `extract_video_url()` method.

### Custom File Naming

Modify the `process_highlight_post()` method to use custom file names by changing `title`

## Troubleshooting

### Common Issues

**"Maximum retries exceeded"**
- Streamable may be blocking requests
- Try increasing retry delay: `RedditVideoDownloader(retry_delay=5)`
- Use a VPN if Streamable isn't accessible in your region

**"Failed to download video"**
- Video URL extraction failed
- The post might not contain a valid Streamable link
- Site structure may have changed, raise an issue in this case

**"Authentication failed"**
- Check your `config.py` credentials
- Ensure your Reddit app is set to "script" type
- Verify username/password are correct
