import json
from pathlib import Path
from nltk import FreqDist
import matplotlib.pyplot as plt
import re
import collections

stopwords = ['a', 'to', 'from', 'i', 'the', 'and', 'you', 'what', 'of', 'is', 'your', 'that', 'in', 'do', 'are', 'have','would', 'for', 'on', 'with', 'or', 'thing', 'reddit', 'who']


def populate_freq_dist_stop_list(subreddit_name):
    freq_dist = FreqDist()
    subreddit = Path('subreddits/{0}'.format(subreddit_name))
    fd_path = Path('subreddits_freq_dist')

    if not Path(fd_path).exists():
        Path(fd_path).mkdir(parents=True)

    directories = [x for x in subreddit.iterdir() if x.is_dir()]
    for directory in directories:
        for file in directory.iterdir():
            with open(file) as f:
                data = json.load(f)
                str = data['title']
                normal = re.sub(r'\b[A-Z]+\b', '', str)
                holder = str.split()
                for token in holder:
                    if token not in stopwords:
                        if token in freq_dist:
                            freq_dist[token] += 1
                        else:
                            freq_dist[token] = 1

    sorted_freq_dist = freq_dist.most_common()
    with open((fd_path / '{0}_freq_dist.json'.format(subreddit_name)), 'w', encoding='utf-8') as file:
        json.dump(sorted_freq_dist, file)

    size ={'size': len(sorted_freq_dist)}

    with open((fd_path / '{0}_freq_dist_size.json'.format(subreddit_name)), 'w', encoding='utf-8') as file:
        json.dump(size, file)



def determine_top_words(title, subreddit):

    subreddit_dist_size = Path('subreddits_freq_dist/{}'.format(subreddit))

    with open(subreddit_dist_size) as f:
        data = json.load(f)

    holder = re.sub(r'\b[A-Z]+\b', '', title)
    holder = str.split()

    top_10_percent = {}
    top_25_percent = {}

    for token in holder:




#populate_freq_dist_stop_list('AskReddit')
