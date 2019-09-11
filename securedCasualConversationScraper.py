import re
import json
import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path
import time

# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

with open('auth.json', 'r') as file:
	auth = json.load(file)

data_folder = Path("D:\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
file_to_open = data_folder / "casual_conversation_top_all.txt";
authorization_folder = Path("D:\Senior Project Holder all");
authorization_file = authorization_folder / "bot_authorization.txt";

# https://stackabuse.com/read-a-file-line-by-line-in-python/

t_list = list()

reddit = praw.Reddit(client_id=auth['client_id'],
                     client_secret=auth['client_secret'],
                     username=auth['username'],
                     password=auth['password'],
                     user_agent='This is a test.')

subreddit = reddit.subreddit('CasualConversation')

# http://www.storybench.org/how-to-scrape-reddit-with-python/

post_info = {"title": [],
             "score": [],
             "id": [], "url": [],
             "comms_num": [],
             "created": [],
             "body": []}

#https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
start_time = time.time()
for submission in reddit.subreddit('CasualConversation').top("year", limit=10):
    post_info["title"].append(submission.title)
    #post_info["score"].append(submission.score)
    #post_info["id"].append(submission.id)
    #post_info["url"].append(submission.url)
    #post_info["comms_num"].append(submission.num_comments)
    #post_info["created"].append(submission.created)
    #post_info["body"].append(submission.selftext)
    with open(file_to_open, 'a', encoding='utf-8') as f:
        temp = str(post_info)
        strippedHolder = re.sub(r'([^\s\w]|_)+', '', temp)
        f.write(str(temp))
    print(str(post_info))
    post_info = {"title": [],
                 "score": [],
                 "id": [], "url": [],
                 "comms_num": [],
                 "created": [],
                 "body": []}

# https://stackoverflow.com/questions/50268298/append-string-to-each-line-of-txt-file-in-python

print("--- %s seconds ---" % (time.time() - start_time))
print("c'est fini")