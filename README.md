# Reddit Scraper

## Description
This script extracts posts and comments from selected subreddits using the Reddit API via the PRAW library. It gathers data from multiple categories, including `top`, `controversial`, `new`, `hot`, and `rising`, and saves the extracted information into CSV files for further analysis.

## Requirements
Before running the script, ensure you have the following dependencies installed:

```sh
pip install praw
```

## Getting Started
To use this script, you need to create a Reddit API application to obtain your credentials.

### How to Get Reddit API Credentials
1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps).
2. Click on `Create an app`.
3. Choose `script` as the type.
4. Fill in the necessary details.
5. Copy the `client_id` and `client_secret` provided by Reddit.
6. Replace the placeholder values in the script with your credentials:
   ```python
   reddit = praw.Reddit(
        client_id='YOUR_CLIENT_ID',
        client_secret='YOUR_CLIENT_SECRET',
        user_agent='YOUR_USER_AGENT',
        username='YOUR_USERNAME',
        password='YOUR_PASSWORD'
   )
   ```

## Usage
1. Modify the `subreddits_list` variable in the script to specify the subreddits you want to scrape.
2. Run the script using:
   ```sh
   python script.py
   ```
3. The extracted data will be saved in two CSV files:
   - `reddit_posts.csv` (contains posts data)
   - `reddit_comments.csv` (contains comments data)

## How It Works
- The script fetches data from existing subreddits specified in `subreddits_list`.
- It retrieves posts based on different categories (`top`, `controversial`, `new`, `hot`, `rising`).
- Each post's metadata (title, author, score, upvote ratio, number of comments, etc.) is stored in `reddit_posts.csv`.
- The script extracts all comments from each post and stores them in `reddit_comments.csv`.
- To prevent duplicate entries, it loads existing post IDs from the CSV file before making new requests.
- A waiting time is implemented between requests to comply with Reddit API rate limits.

## Notes
- The script is fully dependent on the **PRAW** (Python Reddit API Wrapper) library.
- Ensure your Reddit account has API access to fetch data properly.
- If the script runs for a long time, you may need to refresh your credentials or handle API rate limits dynamically.

## License
This project is open-source and free to use under the MIT License.

