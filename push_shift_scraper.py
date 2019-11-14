import json
from pathlib import Path
from time import time
import time
import requests

post_id = {}

POSTS_TO_SCRAPE = 1000


def scrape(after, before, subreddit, size):
    print('starting to scrape {size} results from {subreddit} from {after} days ago to {before} days ago'
          .format(size= size, after= after, before= before, subreddit= subreddit))

    api_url = 'http://api.pushshift.io/reddit/search/submission/?subreddit=' + subreddit + '&after=' + after \
              + '&before=' + before + '&size=' + size + '&sort=desc&sort_type=score'

    request = requests.get(api_url)
    try:
        data = json.loads(request.text)
    except:
        print('Exception')
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

before = 0
after = 20
for x in range(50):
    scrape('{0}d'.format(after), '{0}d'.format(before), 'askreddit', '500')
    before += 20
    after += 20
    time.sleep(1)
