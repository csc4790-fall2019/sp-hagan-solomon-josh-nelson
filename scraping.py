import json
import pandas as pd
import numpy as np
from pathlib import Path
import time

# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
def scrape(reddit):
    print('test')

    subreddit = reddit.subreddit('CasualConversation')

    # http://www.storybench.org/how-to-scrape-reddit-with-python/

    #https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
    data_folder = Path('subreddits')
    subreddit = 'CasualConversation'
    subreddit_path = data_folder / subreddit
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir()

    start_time = time.time()
    counter = 0
    for submission in reddit.subreddit(subreddit).top('year', limit=100):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        #post_info["id"].append(submission.id)
        #post_info["url"].append(submission.url)
        #post_info["comms_num"].append(submission.num_comments)
        #post_info["created"].append(submission.created)
        #post_info["body"].append(submission.selftext)
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1
    # https://stackoverflow.com/questions/50268298/append-string-to-each-line-of-txt-file-in-python

    print("--- %s seconds ---" % (time.time() - start_time))
    print("c'est fini")