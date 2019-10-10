import json
from pathlib import Path
import time
import os, errno

POSTS_TO_SCRAPE = 1000

def scrape(subreddit_name, reddit):
    start_time = time.time()
    scrape_new(subreddit_name, reddit)
    scrape_controversial(subreddit_name, reddit)
    scrape_hot(subreddit_name, reddit)
    scrape_top(subreddit_name, reddit)
    scrape_top_week(subreddit_name, reddit)
    scrape_top_year(subreddit_name, reddit)
    print("Scraping done in %s seconds ---" % (time.time() - start_time))


def scrape_new(subreddit_name, reddit):
    print('Starting New scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('new')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).new(limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_controversial(subreddit_name, reddit):
    print('Starting Controversial scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('controversial')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).controversial('all', limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        post_info['score'] = submission.score - 100
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_top(subreddit_name, reddit):
    print('Starting Top scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('top')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).top('all', limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_top_week(subreddit_name, reddit):
    print('Starting Top scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('top_week')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).top('week', limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_top_year(subreddit_name, reddit):
    print('Starting Top scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('top_week')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).top('year', limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        post_info["score"] = submission.score
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1

def scrape_hot(subreddit_name, reddit):
    print('Starting Hot scraping...')
    subreddit = reddit.subreddit(subreddit_name)
    data_folder = Path('subreddits')
    list_type_folder = Path('hot')
    subreddit_path = data_folder / subreddit.display_name / list_type_folder
    if not Path(subreddit_path).exists():
        Path(subreddit_path).mkdir(parents=True)
    counter = 0
    for submission in reddit.subreddit(subreddit.display_name).hot(limit=POSTS_TO_SCRAPE):
        post_info = {}
        post_info['title'] = submission.title
        if submission.score < 100:
            post_info['score'] = submission.score * 10
        else:
            post_info['score'] = submission.score
        post_info['id'] = submission.id
        with open(subreddit_path / (str(counter) + '.json'), 'w', encoding='utf-8') as file:
            json.dump(post_info, file)
        counter += 1