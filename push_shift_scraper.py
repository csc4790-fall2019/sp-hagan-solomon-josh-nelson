import json
from pathlib import Path
import time
import requests

post_id = {}

POSTS_TO_SCRAPE = 1000


def scrape(after, before, subreddit, size):
    print('starting to scrape {size} results from {subreddit} from {after} days ago to {before} days ago'
          .format(size= size, after= after, before= before, subreddit= subreddit))

    print("yeet")


scrape(100, 90, 'askreddit', 100)
