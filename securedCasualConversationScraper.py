import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path

# https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f

data_folder = Path("D:\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
file_to_open = data_folder / "casual_conversation_top_all.txt";
authorization_folder = Path("D:\Senior Project Holder all");
authorization_file = authorization_folder / "bot_authorization.txt";

# https://stackabuse.com/read-a-file-line-by-line-in-python/

t_client_id = ''
t_client_secret = ''
t_username = ''
t_password = ''
t_user_agent = ''

with open(authorization_file) as fa:
    line = fa.readline().strip().rstrip()
    cnt = 1
    t_client_id = line
    print(t_client_id)
    while line:
        if (cnt == 1):
            line = fa.readline().strip().rstrip()
            t_client_secret = line
            print(t_client_secret)
            cnt += 1
        elif (cnt == 2):
            line = fa.readline().strip().rstrip()
            t_username = line
            print(t_username)
            cnt += 1
        elif (cnt == 3):
            line = fa.readline().strip().rstrip()
            t_password = line
            print(t_password)
            cnt += 1
        else:
            line = fa.readline().strip().rstrip()
            t_user_agent = line
            print(t_user_agent)

reddit = praw.Reddit(client_id=t_client_id,
                     client_secret=t_client_secret,
                     username=t_username,
                     password=t_password,
                     user_agent=t_user_agent);

subreddit = reddit.subreddit('CasualConversation');

# http://www.storybench.org/how-to-scrape-reddit-with-python/


post_info = {"title": [],
             "score": [],
             "id": [], "url": [],
             "comms_num": [],
             "created": [],
             "body": []}

for submission in reddit.subreddit('CasualConversation').top("all", limit=5):
    post_info["title"].append(submission.title)
    post_info["score"].append(submission.score)
    post_info["id"].append(submission.id)
    post_info["url"].append(submission.url)
    post_info["comms_num"].append(submission.num_comments)
    post_info["created"].append(submission.created)
    post_info["body"].append(submission.selftext)
    # f=file_to_open.open("a")
    # f.write(str(post_info))
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


print("c'est fini")
