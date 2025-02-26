import time
import praw
import csv
import os

# User-Agent for Reddit API
UA = 'App by /u/kostasDev28' #UA = 'yourAPP by /u/yourname

# Reddit API authentication
reddit = praw.Reddit(
     client_id='YOUR_CLIENT_ID',
     client_secret='YOUR_CLIENT_SECRET',
     user_agent='YOUR_USER_AGENT',
     username='YOUR_USERNAME',
     password='YOUR_PASSWORD'
)

# List of subreddits to scrape
subreddits_list = ['AmericanPolitics', 'PoliticsHangout', 'Voting', 'tuesday']  # Modify as needed
all_submissions = []
all_comments = []

# CSV filenames
posts_csv_file = "reddit_posts6.csv"
comments_csv_file = "reddit_comments6.csv"

# Load existing post IDs to prevent duplicate entries
existing_post_ids = set()
if os.path.exists(posts_csv_file):
     with open(posts_csv_file, mode='r', encoding='utf-8') as file:
         reader = csv.DictReader(file)
         for row in reader:
             if 'id' in row:
                 existing_post_ids.add(row['id'])

# Function to scrape posts and comments from a subreddit
def fetch_submissions(subreddit, category, time_filter=None, limit=2000, batch_size=100):
     submissions = []
     comments = []
     after = None
     count = 0

     while count < limit:
         if category in ['top', 'controversial']:
             submission_generator = getattr(subreddit, category)(time_filter=time_filter, limit=batch_size, params={'after': after})
         else:
             submission_generator = getattr(subreddit, category)(limit=batch_size, params={'after': after})

         fetched = 0
         for submission in submission_generator:
             if submission.id in existing_post_ids:
                 continue

             submission_data = {
                 'id': submission.id,
                 'category': category,
                 'subreddit': subreddit.display_name,
                 'title': submission.title,
                 'author': str(submission.author),
                 'created_utc': submission.created_utc,
                 'score': submission.score,
                 'upvote_ratio': submission.upvote_ratio,
                 'num_comments': submission.num_comments,
                 'url': submission.url,
                 'selftext': submission.selftext
             }

             submissions.append(submission_data)
             after = submission.fullname
             fetched += 1
             count += 1

             # Scrape comments for each post
             submission.comments.replace_more(limit=0)
             for comment in submission.comments.list():
                 comment_data = {
                     'post_id': submission.id,
                     'comment_id': comment.id,
                     'comment_author': str(comment.author),
                     'comment_body': comment.body,
                     'comment_created_utc': comment.created_utc,
                     'comment_score': comment.score
                 }
                 comments.append(comment_data)

             print(f"Fetched {count} posts so far from {subreddit.display_name}...")

             if count >= limit:
                 break

         if fetched == 0:
             break

         # Avoid hitting API request limits
         time.sleep(25)

     return submissions, comments

# Categories and time filters
categories = [
     {'category': 'top', 'time_filter': 'all', 'limit': 2000},
     {'category': 'top', 'time_filter': 'week', 'limit': 2000},
     {'category': 'top', 'time_filter': 'year', 'limit': 2000},
     {'category': 'top', 'time_filter': 'month', 'limit': 2000},
     {'category': 'controversial', 'time_filter': 'all', 'limit': 2000},
     {'category': 'controversial', 'time_filter': 'year', 'limit': 2000},
     {'category': 'new', 'time_filter': None, 'limit': 2000},
     {'category': 'hot', 'time_filter': None, 'limit': 2000},
     {'category': 'rising', 'time_filter': None, 'limit': 2000},
]

# Scraping data from each subreddit
for subreddit_name in subreddits_list:
     subreddit = reddit.subreddit(subreddit_name)
     for cat in categories:
         print(f"Scraping category: {cat['category']} with filter: {cat.get('time_filter', 'N/A')} in subreddit: {subreddit_name}")
         try:
             submissions, comments = fetch_submissions(
                 subreddit,
                 category=cat['category'],
                 time_filter=cat.get('time_filter'),
                 limit=cat['limit']
             )
             all_submissions.extend(submissions)
             all_comments.extend(comments)
         except Exception as e:
             print(f"Error scraping category: {cat['category']} in subreddit: {subreddit_name}: {e}")

     # Wait 5 minutes before moving to the next subreddit to avoid rate limits
     print("Waiting before moving to the next subreddit...")
     time.sleep(400)  # 5-minute wait

# Append new post data to CSV
if all_submissions:
     with open(posts_csv_file, mode='a', newline='', encoding='utf-8') as file:
         writer = csv.DictWriter(file, fieldnames=all_submissions[0].keys())
         if os.stat(posts_csv_file).st_size == 0:
             writer.writeheader()
         writer.writerows(all_submissions)
     print(f"Added {len(all_submissions)} new post entries into file: {posts_csv_file}")
else:
     print("No new posts found.")

# Append new comment data to CSV
if all_comments:
     with open(comments_csv_file, mode='a', newline='', encoding='utf-8') as file:
         comment_fieldnames = ['post_id', 'comment_id', 'comment_author', 'comment_body', 'comment_created_utc', 'comment_score']
         writer = csv.DictWriter(file, fieldnames=comment_fieldnames)
         if os.stat(comments_csv_file).st_size == 0:
             writer.writeheader()
         writer.writerows(all_comments)
     print(f"Added {len(all_comments)} new comment entries into file: {comments_csv_file}")
else:
     print("No new comments found.")
