import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

STOPWORDS = ['the', 'it', 'a', 'an', 'was', 'were', 'had', 'is', 'have', 'are']


def get_data(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    files = [x for x in p.iterdir() if x.is_file()]

    text_data = []
    labels = []

    rating_1 = 0
    rating_0 = 0
    for file in files:
        with open(file) as f:
            data = json.load(f)
            text_data.append(data['title'])
            if data['score'] >= 300:
                rating_1 += 1
                labels.append('1')
            else:
                rating_0 += 1
                labels.append('0')

    df = pd.DataFrame({'title': text_data, 'rating': labels})

    def clean_text(text):
        text = ' '.join(word for word in text.split() if word not in STOPWORDS)
        return text

    df['title'] = df['title'].apply(clean_text)
    df = df.reindex(np.random.permutation(df.index))
    return df


def get_data_guess(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    files = [x for x in p.iterdir() if x.is_file()]

    mode = get_data_guess(subreddit_name)

    text_data = []
    labels = []

    rating_1 = 0
    rating_0 = 0
    for file in files:
        with open(file) as f:
            data = json.load(f)
            text_data.append(data['title'])
            if data['score'] >= get_data_guess():
                rating_1 += 1
                labels.append('1')
            else:
                rating_0 += 1
                labels.append('0')

    df = pd.DataFrame({'title': text_data, 'rating': labels})

    def clean_text(text):
        text = ' '.join(word for word in text.split() if word not in STOPWORDS)
        return text

    df['title'] = df['title'].apply(clean_text)
    df = df.reindex(np.random.permutation(df.index))
    return df


def mat_plot_accuracy(part1, part2, part3):
    # parameters must represent a number between 0 and 100 inclusive
    fig1, ax1 = plt.subplots()
    labels = 'Correct', 'Incorrect'
    sizes = [part1, 100 - part1]
    explode = (0.1, 0)  # only "explode" the 2nd slice
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Viral Posts')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('success_percentage.png')

    fig2, ax2 = plt.subplots()
    labels = 'Correct', 'Incorrect'
    sizes = [part2, 100 - part2]
    explode = (0.1, 0)  # only "explode" the 2nd slice
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Non-viral Posts')
    plt.savefig('failure_percentage.png')

    fig3, ax3 = plt.subplots()
    labels = 'Correct', 'Incorrect'
    sizes = [part3, 100 - part3]
    explode = (0.1, 0)  # only "explode" the 2nd slice
    ax3.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Mean Accuracy During Training')
    plt.savefig('average_percentage.png')
