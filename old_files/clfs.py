import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.svm import NuSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def naive_bayes():
    nb = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                   ('tfidf', TfidfTransformer(sublinear_tf=True)),
                   ('clf', MultinomialNB()),
                  ])
    return nb

def sgd():
    sgd = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                    ('tfidf', TfidfTransformer(sublinear_tf=True)),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=0.000001, random_state=36, max_iter=100, tol=None, learning_rate='optimal')),
                   ])
    return sgd

def logreg():
    logreg = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                       ('tfidf', TfidfTransformer(sublinear_tf=True)),
                       ('clf', LogisticRegression(n_jobs=1, C=1000, solver='liblinear', dual=False)),
                      ])
    return logreg

def svc():
    svc = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                       ('tfidf', TfidfTransformer(sublinear_tf=True)),
                       ('clf', SVC()),
                      ])
    return svc

def linsvc():
    linsvc = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                       ('tfidf', TfidfTransformer(sublinear_tf=True)),
                       ('clf', LinearSVC(max_iter=5000, dual=False)),
                      ])
    return linsvc

def nusvc():
    nusvc = Pipeline([('vect', CountVectorizer(strip_accents='unicode', lowercase=True)),
                       ('tfidf', TfidfTransformer(sublinear_tf=True)),
                       ('clf', NuSVC()),
                      ])
    return nusvc

def test(data):
    X_train, X_test, y_train, y_test = train_test_split(data['Title'], data['Rating'], test_size=0.3)

    svc_ = linsvc()
    svc_.fit(X_train, y_train)
    print(svc_.score(X_test, y_test))
    print('linsvc: ' + str(determine_percentages(predicted, y_test)))

    linsvc_ = linsvc()
    linsvc_.fit(X_train, y_train)
    predicted = linsvc_.predict(X_test)
    print('linsvc: ' + str(determine_percentages(predicted, y_test)))

    nusvc_ = nusvc()
    nusvc_.fit(X_train, y_train)
    predicted = nusvc_.predict(X_test)
    print('nusvc: ' + str(determine_percentages(predicted, y_test)))

    sgd_ = sgd()
    sgd_.fit(X_train, y_train)
    predicted = sgd_.predict(X_test)
    print('sgd: ' + str(determine_percentages(predicted, y_test)))

    logreg_ = logreg()
    logreg_.fit(X_train, y_train)
    predicted = logreg_.predict(X_test)
    print('logreg: ' + str(determine_percentages(predicted, y_test)))

def determine_percentages(predicted, expected):
    total_good = 0
    total_bad = 0

    found_good = 0
    found_bad = 0

    expected = np.array(expected)
    for x in range(len(expected)):
        if expected[x] == '1':
            if predicted[x] == '1':
                found_good += 1
            total_good += 1
        else:
            if predicted[x] == '0':
                found_bad += 1
            total_bad += 1

    return ((found_good / total_good), (found_bad / total_bad), ((found_good + found_bad) / (total_good + total_bad)))

def get_total_percentages(data, runs):
    nb = naive_bayes()
    svm = sgd()
    lgrg = logreg()

    success_pct = 0
    failure_pct = 0
    avg_pct = 0

    for x in range(runs):
        X_train, X_test, y_train, y_test = train_test_split(data['Title'], data['Rating'], test_size=0.3)

        linsvc_ = linsvc()
        linsvc_.fit(X_train, y_train)
        linsvc_predicted = linsvc_.predict(X_test)
        print('linsvc: ' + str(determine_percentages(linsvc_predicted, y_test)))
        linsvc_success_pct, linsvc_failure_pct, linsvc_avg_pct = determine_percentages(linsvc_predicted, y_test)

        svm.fit(X_train, y_train)
        svm.score()
        svm_predicted = svm.predict(X_test)
        print('SGD: ' + str(determine_percentages(svm_predicted, y_test)))
        svm_success_pct, svm_failure_pct, svm_avg_pct = determine_percentages(svm_predicted, y_test)

        lgrg.fit(X_train, y_train)
        lgrg_predicted = lgrg.predict(X_test)
        print('lgrg: ' + str(determine_percentages(lgrg_predicted, y_test)))
        lgrg_success_pct, lgrg_failure_pct, lgrg_avg_pct = determine_percentages(lgrg_predicted, y_test)

        predicted = []
        for y in range(len(lgrg_predicted)):
            found_goods = 0
            if linsvc_predicted[y] == '1':
                found_goods += 1
            if svm_predicted[y] == '1':
                found_goods += 1
            if lgrg_predicted[y] == '':
                found_goods +=1

            if (found_goods >= 1):
                predicted.append('1')
            else:
                predicted.append('0')
        
        (succ, fail, avg) = determine_percentages(predicted, y_test)
        success_pct += succ
        failure_pct += fail
        avg_pct += avg

    return ((success_pct / runs), (failure_pct / runs), (avg_pct / runs))

def predict_title(data, title, runs):
    nb = naive_bayes()
    svm = sgd()
    lgrg = logreg()
    linsvc_ = linsvc()

    total_goods = 0
    for x in range(runs):
        X_train, X_test, y_train, y_test = train_test_split(data['Title'], data['Rating'], test_size=0.3)
        
        linsvc_.fit(X_train, y_train)
        linsvc_predicted = linsvc_.predict([title])
        # nb.fit(X_train, y_train)
        # nb_predicted = nb.predict([title])
        # print(nb_predicted)
        # nb_success_pct, nb_failure_pct, nb_avg_pct = determine_percentages(predicted, y_test)

        svm.fit(X_train, y_train)
        svm_predicted = svm.predict([title])
        # print(svm_predicted)
        # svm_success_pct, svm_failure_pct, svm_avg_pct = determine_percentages(predicted, y_test)

        lgrg.fit(X_train, y_train)
        lgrg_predicted = lgrg.predict([title])
        # print(lgrg_predicted)
        # lgrg_success_pct, lgrg_failure_pct, lgrg_avg_pct = determine_percentages(predicted, y_test)
        
        found_goods = 0
        if linsvc_predicted[0] == '1':
            found_goods += 1
        if svm_predicted[0] == '1':
            found_goods += 1
        if lgrg_predicted[0] == '1':
            found_goods +=1

        if (found_goods >= 1):
            total_goods += 1

    if total_goods >= runs / 2:
        prediction = '1'
    else:
        prediction = '0'

    return prediction

def mat_plot_test_accuracy(part1, part2, part3):
    #parameters must represent a number between 0 and 100 inclusive
    fig1, ax1 = plt.subplots()
    labels = 'Correct', 'Incorrect'
    sizes = [part1, 100-part1]
    explode = (0.1, 0)  # only "explode" the 2nd slice
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    plt.title('Viral Training Posts')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('success_percentage.png')

    fig2, ax2 = plt.subplots()
    labels = 'Correct', 'Incorrect'
    sizes = [part2, 100 - part2]
    explode = (0.1, 0)  # only "explode" the 2nd slice
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Non-viral Training Posts')
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

