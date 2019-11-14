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

#starting to add sketchy stuff

    sorted_freq_dist = collections.OrderedDict(freq_dist.most_common())

    num_top_10 = round(len(sorted_freq_dist) * 0.1)
    num_top_25 = round(len(sorted_freq_dist) * 0.25)
    top_10_percent = []
    top_25_percent = []

    counter = 0

    for key, value in sorted_freq_dist.items():
        counter += 1
        if key in sorted_freq_dist.keys():
            if counter <= num_top_10:
                top_10_percent.append(key)
        if key in sorted_freq_dist.keys():
            if counter <= num_top_25:
                top_25_percent.append(key)

#end sketchy stuff

    with open((fd_path / '{0}_freq_dist.json'.format(subreddit_name)), 'w', encoding='utf-8') as file:
        json.dump(sorted_freq_dist, file)

    size ={'size': len(sorted_freq_dist), 'top_10' : top_10_percent, 'top_25' : top_25_percent}

    with open((fd_path / '{0}_freq_dist_size.json'.format(subreddit_name)), 'w', encoding='utf-8') as file:
        json.dump(size, file)



def determine_top_words(title, subreddit):

    subreddit_dist_size = Path('subreddits_freq_dist/{}_freq_dist_size.json'.format(subreddit))
    subreddit_dist = Path('subreddits_freq_dist/{}_freq_dist.json'.format(subreddit))


    with open(subreddit_dist_size) as f:
        size_data = collections.OrderedDict(json.load(f))
        length_of_dict = size_data['size']

    with open(subreddit_dist) as g:
        data = collections.OrderedDict(json.load(g))

    re.sub(r'\b[A-Z]+\b', '', title)
    title = title.split()

    top_10_percent = {}
    top_25_percent = {}

    num_top_10 = round(length_of_dict * 0.1)
    num_top_25 = round(length_of_dict * 0.25)

    for token in title:
        for key, value in data.items():
            if token in data.keys():
                if data.index(token) <= num_top_10:
                    top_10_percent.add(token)
            if key in data.keys():
                if data.keys().index(token) <= num_top_25:
                    top_25_percent.add(token)

    print(top_10_percent)
    print(top_25_percent)

populate_freq_dist_stop_list('AskReddit')

#determine_top_words('What it be people made random fluff noise', 'AskReddit')