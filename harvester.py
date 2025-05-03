import requests
import json
from module_utils import Modules


def poll_subreddit_new(subreddit_name: str, limit: int = 10):
    Modules.log(0, f"Polling subreddit {subreddit_name} for {limit} posts")
    """
    Poll a subreddit for posts and return them as a list of dictionaries.
    """
    url = f"https://www.reddit.com/r/{subreddit_name}/new.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    # Might be a good idea to use a proxy here
    proxies = {
    }
    response = requests.get(url, headers=headers, proxies=proxies)
    response.raise_for_status()
    data = response.json()
    # we should filter out the fields that we want to keep: title, author, selftext, subreddit, url, created_utc
    filtered_data = []

    for post in data['data']['children']:
        filtered_data.append({
            'title': post['data']['title'],
            'author': post['data']['author'],
            'subreddit': post['data']['subreddit'],
            'url': post['data']['url'],
            'created_utc': post['data']['created_utc'],
            'selftext': post['data']['selftext'],
        })
    Modules.log(0, f"Found {len(filtered_data)} posts")
    return filtered_data

if __name__ == "__main__":
    data = poll_subreddit_new("startups")