import re
import json
import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path
import time

from scraping import scrape
from sprint1_scraper import scrape1

with open('auth.json', 'r') as file:
    auth = json.load(file)

reddit = praw.Reddit(client_id=auth['client_id'],
                     client_secret=auth['client_secret'],
                     username=auth['username'],
                     password=auth['password'],
                     user_agent='This is a test.')

#scrape('AskHistorians', reddit)
scrape1('AskHistorians', reddit)
