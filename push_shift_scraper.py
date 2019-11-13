import json
from pathlib import Path
import time
import requests

post_id = {}

POSTS_TO_SCRAPE = 1000


def scrape(after, before, subreddit, size):
    print('starting to scrape {size} results from {subreddit} from {after} days ago to {before} days ago'
          .format(size= size, after= after, before= before, subreddit= subreddit))

    api_url = 'http://api.pushshift.io/reddit/search/submission/?subreddit=' + subreddit + '&after=' + after \
              + '&before=' + before + '&size=' + size

    print("yeet")



scrape(100, 90, 'askreddit', 100)
