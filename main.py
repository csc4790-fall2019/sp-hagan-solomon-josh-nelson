import re
import json
import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path
import time

from scraper import scrape
from naive_bayes import get_data
from naive_bayes import run_naive_bayes

with open('auth.json', 'r') as file:
    auth = json.load(file)

reddit = praw.Reddit(client_id=auth['client_id'],
                     client_secret=auth['client_secret'],
                     username=auth['username'],
                     password=auth['password'],
                     user_agent='This is a test.')

#scrape('AskHistorians', reddit)
#scrape('AskReddit', reddit)
data = get_data('AskReddit')
run_naive_bayes('AskReddit', data)
