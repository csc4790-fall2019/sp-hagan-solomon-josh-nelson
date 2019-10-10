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
from example_classifier import split_train_test
from example_classifier import buildProbabilityTable
from example_classifier import naiveBayesClassify
from example_classifier import naiveBayesTest

with open('auth.json', 'r') as file:
    auth = json.load(file)

reddit = praw.Reddit(client_id=auth['client_id'],
                     client_secret=auth['client_secret'],
                     username=auth['username'],
                     password=auth['password'],
                     user_agent='This is a test.')

#scrape('AskHistorians', reddit)
#scrape('AskReddit', reddit)
# data = get_data('CasualConversation')
train_data, test_data = split_train_test('AskReddit', seed=3)
naiveBayesTest(train_data, test_data)

train_data, test_data = split_train_test('AskReddit', split_percent=1)
probs = buildProbabilityTable(train_data)
print(naiveBayesClassify(probs, input("Enter a phrase: ")))