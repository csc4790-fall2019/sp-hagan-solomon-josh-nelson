# import praw
import json
import utils
import clf
# from zipf import populate_freq_dist_stop_list
from pathlib import Path
from scraper import run_scraper
from sklearn.model_selection import train_test_split

def main(input_title, subreddit):
    with open('auth.json', 'r') as file:
        auth = json.load(file)

    # reddit = praw.Reddit(client_id=auth['client_id'],
    #                      client_secret=auth['client_secret'],
    #                      username=auth['username'],
    #                      password=auth['password'],
    #                      user_agent='This is a test.')

    if not Path('subreddits/{0}'.format(subreddit)).exists():
        run_scraper(subreddit)

    # populate_freq_dist_stop_list('this is a title', 'AskReddit')

    prediction = clf.predict(input_title, subreddit)
    print('Prediction for "{0}": {1}'.format(input_title, prediction))

    return prediction
