import json
from pathlib import Path
from time import time
import time
import requests
import datetime

post_id = {}

# take note after comes before because it is technically the first date
# size: number to return
# order: asc, desc
def scrape(after, before, subreddit, size, order):
    print('starting to scrape {size} results from {subreddit} from {after} days ago to {before} days ago'
          .format(size=size, after=after, before=before, subreddit=subreddit))

    api_url = 'http://api.pushshift.io/reddit/search/submission/?subreddit=' + subreddit + '&after=' + after \
              + '&before=' + before + '&size=' + size + '&sort=' + order + '&sort_type=score'

    request = requests.get(api_url)
    data = json.loads(request.text)

    try:
        data = json.loads(request.text)
    except:
        print('Exception getting data')
        return

    path = Path('subreddits/{0}'.format(subreddit.lower()))
    if not path.exists():
        path.mkdir(parents=True)

    for submission in data['data']:
        post_data = {
            'id': submission['id'],
            'title': submission['title'],
            'score': submission['score'],
        }

        with open(path / '{0}.json'.format(post_data['id']), 'w', encoding='utf-8') as file:
            json.dump(post_data, file)

# scrape('20d', '0d', 'askreddit', '500')

def run_scraper():
    before = 0
    after = 20
    for x in range(50):
        scrape('{0}d'.format(after), '{0}d'.format(before), 'askreddit', '500', 'desc')
        scrape('{0}d'.format(after), '{0}d'.format(before), 'askreddit', '500', 'asc')
        before += 20
        after += 20
        time.sleep(1)
