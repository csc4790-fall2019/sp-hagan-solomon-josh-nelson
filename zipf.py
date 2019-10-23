import json
from pathlib import Path
from nltk import FreqDist
import matplotlib.pyplot as plt

def populate_freq_dist(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    directories = [x for x in p.iterdir() if x.is_dir()]
    for directory in directories:
        for file in directory.iterdir():
            with open(file) as f:
                data = json.load(f)
                str = data['title']
                holder = str.split()
                for token in holder:
                    fd[token] += 1

    fd.most_common(10)

    plt.ion()
    fd.plot(25, title='Top 25 Most Common Words in Corpus')
    plt.savefig('top_25_words_used.png')
    plt.ioff()
    pass


def populate_freq_dist_stop_list(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    directories = [x for x in p.iterdir() if x.is_dir()]
    counter = 0

    for directory in directories:
        for file in directory.iterdir():
            with open(file) as f:
                data = json.load(f)
                str = data['title']
                holder = str.split()
                for token in holder:
                    if token not in stopwords:
                        fd[token] += 1

    fd.most_common(10)

    plt.ion()
    fd.plot(25, title='Top 25 Most Common Words in Corpus: No Stop words')
    plt.savefig('top_25_words_used_stop_words.png')
    plt.ioff()
    pass
stopwords = ['a', 'to', 'from', 'i', 'the', 'and']
fd = FreqDist()
populate_freq_dist('Askreddit')
populate_freq_dist_stop_list('Askreddit')