import json
from pathlib import Path
import time
import os, errno


def scrape1(subreddit_name, reddit):
    start_time = time.time()
    scrape_new(subreddit_name, reddit)
    scrape_controversial(subreddit_name, reddit)
    scrape_hot(subreddit_name, reddit)
    scrape_top(subreddit_name, reddit)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("c'est fini")



def scrape_new(subreddit_name, reddit):
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('new')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).new(limit=100):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_controversial(subreddit_name, reddit):
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('controversial')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).controversial('month', limit=100):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_top(subreddit_name, reddit):
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('top')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).top('week', limit=100):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_hot(subreddit_name, reddit):
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('hot')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).hot(limit=100):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1
