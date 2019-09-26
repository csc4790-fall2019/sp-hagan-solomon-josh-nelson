import json
import math
import numpy as np
import pandas as pd

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from pathlib import Path

def run_naive_bayes(subreddit_name, reddit):
    p = Path('subreddits/{0}'.format(subreddit_name))
    directories = [x for x in p.iterdir() if x.is_dir()]

    text_data = []
    labels = []
    weights = []

    for directory in directories:
        for file in directory.iterdir():
            with open(file) as f:
                data = json.load(f)
                text_data.append(data['title'])
                if data['score'] >= 500:
                    labels.append('good')
                else:
                    labels.append('bad')

                if data['score'] > 10000:
                    weights.append(50)
                elif data['score'] > 1000:
                    weights.append(30)
                elif data['score'] < 50:
                    weights.append(15)
                elif data['score'] < -100:
                    weights.append(30)
                else:
                    weights.append(1)

    Reddit_Data = {'Title': text_data,'Score': labels, 'Weight': weights}
    df = pd.DataFrame(Reddit_Data, columns=['Title', 'Score', 'Weight'])
    df = df.reindex(np.random.permutation(df.index))

    SPLIT_RATIO = 0.6
    split_point = math.floor(len(df.index) * SPLIT_RATIO)

    train_data = df['Title'][0:split_point]
    train_labels = df['Score'][0:split_point]
    train_weights = df['Weight'][0:split_point]

    test_data = df['Title'][split_point:len(text_data)]
    test_labels = df['Score'][split_point:len(labels)]

    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(train_data)

    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

    clf = MultinomialNB().fit(X_train_tfidf, train_labels, train_weights)
    # clf = MultinomialNB().fit(X_train_counts, train_labels, train_weights)

    predicted = clf.predict(count_vect.transform(test_data))

    # Output testing
    print(np.mean(predicted == test_labels))

    total_very_good = 0
    total_very_good_right = 0
    total_good = 0
    total_good_right = 0
    total_bad = 0
    total_bad_right = 0
    total_very_bad = 0
    total_very_bad_right = 0

    real_data = np.array(test_labels)
    for x in range(len(predicted)):
        if real_data[x] == 'good':
            total_good += 1
            if predicted[x] == 'good':
                total_good_right += 1
        elif real_data[x] == 'bad':
            total_bad += 1
            if predicted[x] == 'bad':
                total_bad_right += 1
        # elif real_data[x] == 'very good':
        #     total_very_good += 1
        #     if predicted[x] == 'very good':
        #         total_very_good_right += 1
        # elif real_data[x] == 'very bad':
        #     total_very_bad += 1
        #     if predicted[x] == 'very bad':
        #         total_very_bad_right += 1

    # print('Total correct very good: {0} / {1}'.format(total_very_good_right, total_very_good) +
    # ' ({0})'.format(total_very_good_right / total_very_good))

    print('Total correct good: {0} / {1}'.format(total_good_right, total_good) +
        ' ({0})'.format(total_good_right / total_good))


    print('Total correct bad: {0} / {1}'.format(total_bad_right, total_bad) +
        ' ({0})'.format(total_bad_right / total_bad))


    mat_plot_test_accuracy(total_good_right, 'good', total_good, total_bad_right, 'bad', total_bad)

    #mat_plot_test_accuracy(total_bad_right, "bad", total_bad)

    # print('Total correct very bad: {0} / {1}'.format(total_very_bad_right, total_very_bad) +
    #     ' ({0})'.format(total_very_bad_right / total_very_bad))


def mat_plot_test_accuracy(good_good, val_type1, gtotal, bad_good, val_type2, bad_total):
    fig1, ax1 = plt.subplots()
    labels = 'good-right', 'good-missed'
    sizes = [good_good, gtotal-good_good]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    fig2, ax2 = plt.subplots()
    labels = 'bad-right', 'bad-missed'
    sizes = [bad_good, bad_total-bad_good]
    explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    