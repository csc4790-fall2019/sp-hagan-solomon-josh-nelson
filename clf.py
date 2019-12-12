import pickle
import utils
import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split

from scraper import scrape, run_scraper


def create_models(subreddit):
    models_path = Path('models/{0}'.format(subreddit.lower()))
    if not models_path.exists():
        models_path.mkdir(parents=True)

    data = utils.get_data(subreddit.lower())

    titles = np.array(data['title'])
    ratings = np.array(data['rating'])

    train_x, test_x, train_y, test_y = train_test_split(titles, ratings, test_size=0.3)

    # Fit models and save them
    nb = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                   ('tfidf', TfidfTransformer(sublinear_tf=True)),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(train_x, train_y)
    with open(models_path / 'nb.pkl', 'wb') as file:
        pickle.dump(nb, file)

    lg = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                   ('tfidf', TfidfTransformer(sublinear_tf=True)),
                   ('clf', LogisticRegression(n_jobs=1, C=1000, solver='liblinear', dual=False)),
                   ])
    lg.fit(train_x, train_y)
    with open(models_path / 'lg.pkl', 'wb') as file:
        pickle.dump(lg, file)

    # Test accuracy
    y_score_1 = nb.predict(test_x)
    y_score_2 = lg.predict(test_x)

    count_0, count_1 = 0, 0
    total_0, total_1 = 0, 0
    for i in range(len(y_score_2)):
        found_1 = 0
        if y_score_1[i] == '1':
            found_1 += 1
        if y_score_2[i] == '1':
            found_1 += 1

        if found_1 >= 1 and test_y[i] == '1':
            count_1 += 1
        elif found_1 < 1 and test_y[i] == '0':
            count_0 += 1

        if test_y[i] == '1':
            total_1 += 1
        else:
            total_0 += 1

    nonviral_pct = round(count_0 / total_0 * 100, 2)
    viral_pct = round(count_1 / total_1 * 100, 2)
    total_pct = round((count_0 + count_1) / (total_0 + total_1) * 100, 2)

    print('---Successfully saved models with the following combined accuracies---')
    print('Rating 0 Accuracy: {0} / {1} ({2})'.format(count_0, total_0, nonviral_pct))
    print('Rating 1 Accuracy: {0} / {1} ({2})'.format(count_1, total_1, viral_pct))
    print('Total Accuracy: {0} / {1} ({2})'.format(count_0 + count_1, total_0 + total_1, total_pct))

    utils.mat_plot_accuracy(viral_pct, nonviral_pct, total_pct)


def create_models_guess(subreddit):
    models_path = Path('models/{0}'.format(subreddit.lower()))
    if not models_path.exists():
        models_path.mkdir(parents=True)

    data = utils.get_data_guess(subreddit.lower())

    titles = np.array(data['title'])
    ratings = np.array(data['rating'])

    train_x, test_x, train_y, test_y = train_test_split(titles, ratings, test_size=0.3)

    # Fit models and save them
    nb = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                   ('tfidf', TfidfTransformer(sublinear_tf=True)),
                   ('clf', MultinomialNB()),
                   ])
    nb.fit(train_x, train_y)
    with open(models_path / 'nb_guess.pkl', 'wb') as file:
        pickle.dump(nb, file)

    lg = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                   ('tfidf', TfidfTransformer(sublinear_tf=True)),
                   ('clf', LogisticRegression(n_jobs=1, C=1000, solver='liblinear', dual=False)),
                   ])
    lg.fit(train_x, train_y)
    with open(models_path / 'lg_guess.pkl', 'wb') as file:
        pickle.dump(lg, file)

    # Test accuracy
    y_score_1 = nb.predict(test_x)
    y_score_2 = lg.predict(test_x)

    count_0, count_1 = 0, 0
    total_0, total_1 = 0, 0
    for i in range(len(y_score_2)):
        found_1 = 0
        if y_score_1[i] == '1':
            found_1 += 1
        if y_score_2[i] == '1':
            found_1 += 1

        if found_1 >= 1 and test_y[i] == '1':
            count_1 += 1
        elif found_1 < 1 and test_y[i] == '0':
            count_0 += 1

        if test_y[i] == '1':
            total_1 += 1
        else:
            total_0 += 1

    nonviral_pct = round(count_0 / total_0 * 100, 2)
    viral_pct = round(count_1 / total_1 * 100, 2)
    total_pct = round((count_0 + count_1) / (total_0 + total_1) * 100, 2)

    print('---Successfully saved models with the following combined accuracies---')
    print('Rating 0 Accuracy: {0} / {1} ({2})'.format(count_0, total_0, nonviral_pct))
    print('Rating 1 Accuracy: {0} / {1} ({2})'.format(count_1, total_1, viral_pct))
    print('Total Accuracy: {0} / {1} ({2})'.format(count_0 + count_1, total_0 + total_1, total_pct))

    utils.mat_plot_accuracy(viral_pct, nonviral_pct, total_pct)


def predict(title, subreddit):
    models_path = Path('models/{0}'.format(subreddit.lower()))
    if not models_path.exists():
        create_models(subreddit)

    with open(models_path / 'nb.pkl', 'rb') as file:
        nb = pickle.load(file)
    with open(models_path / 'lg.pkl', 'rb') as file:
        lg = pickle.load(file)

    y_score_1 = nb.predict([title])
    y_score_2 = lg.predict([title])

    result = 0
    found_1 = 0
    if y_score_1[0] == '1':
        found_1 += 1
    if y_score_2[0] == '1':
        found_1 += 1

    if found_1 >= 1:
        result = 1

    return result


def predict_guess(title, subreddit):
    models_path = Path('models/{0}'.format(subreddit.lower()))
    if not models_path.exists():
        create_models_guess(subreddit)

    with open(models_path / 'nb_guess.pkl', 'rb') as file:
        nb = pickle.load(file)
    with open(models_path / 'lg_guess.pkl', 'rb') as file:
        lg = pickle.load(file)

    y_score_1 = nb.predict([title])
    y_score_2 = lg.predict([title])

    result = 0
    found_1 = 0
    if y_score_1[0] == '1':
        found_1 += 1
    if y_score_2[0] == '1':
        found_1 += 1

    if found_1 >= 1:
        result = 1

    return result


def guess_divide(subreddit_name):
    split_line = 300
    before = 0
    after = 20

    df = karma_guess_filter(subreddit_name)
    median = df['score'].mean()

    print(median)

    return median


def karma_guess_filter(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    files = [x for x in p.iterdir() if x.is_file()]

    karma = []

    for file in files:
        with open(file) as f:
            data = json.load(f)
            if 1000 >= data['score'] > 0:
                karma.append(data['score'])
    df = pd.DataFrame({'score': karma})
    return df
