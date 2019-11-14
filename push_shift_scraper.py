import json
from pathlib import Path
import time
import requests
import datetime

post_id = {}

POSTS_TO_SCRAPE = 1000


#take note after comes becore because it is technically the first date
def scrape(after, before, subreddit, size):
    print('starting to scrape {size} results from {subreddit} from {after} days ago to {before} days ago'
          .format(size= size, after= after, before= before, subreddit= subreddit))

    api_url = 'http://api.pushshift.io/reddit/search/submission/?subreddit=' + subreddit + '&after=' + after \
              + '&before=' + before + '&size=' + size

    request = requests.get(api_url)
    data = json.loads(request.text)

    print(data)


#scrape('100d', '90d' , 'askreddit', '100')

