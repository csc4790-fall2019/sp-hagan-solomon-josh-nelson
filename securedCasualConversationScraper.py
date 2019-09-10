import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path
import time

# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

data_folder = Path("D:\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
file_to_open = data_folder / "casual_conversation_top_all.txt";
authorization_folder = Path("D:\Senior Project Holder all");
authorization_file = authorization_folder / "bot_authorization.txt";

# https://stackabuse.com/read-a-file-line-by-line-in-python/

t_list = list()

with open(authorization_file) as fa:
    line1 = fa.readline().strip()
    line2 = fa.readline().strip()
    line3 = fa.readline().strip()
    line4 = fa.readline().strip()
    line5 = fa.readline().strip()

reddit = praw.Reddit(client_id=line1,
                     client_secret=line2,
                     username=line3,
                     password=line4,
                     user_agent=line5);

subreddit = reddit.subreddit('CasualConversation');

# http://www.storybench.org/how-to-scrape-reddit-with-python/


post_info = {"title": [],
             "score": [],
             "id": [], "url": [],
             "comms_num": [],
             "created": [],
             "body": []}

#https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution
start_time = time.time()
for submission in reddit.subreddit('CasualConversation').top("all", limit=1):
    post_info["title"].append(submission.title)
    post_info["score"].append(submission.score)
    post_info["id"].append(submission.id)
    post_info["url"].append(submission.url)
    post_info["comms_num"].append(submission.num_comments)
    post_info["created"].append(submission.created)
    post_info["body"].append(submission.selftext)
    with open(file_to_open, 'a', encoding='utf-8') as f:
        f.write(str(post_info))
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