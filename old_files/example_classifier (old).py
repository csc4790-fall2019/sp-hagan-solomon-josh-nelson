from nltk import word_tokenize, NaiveBayesClassifier
from nltk import classify
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from pathlib import Path
import random
import operator
import os, glob, re
import numpy as np
import json

def split_train_test(subreddit, split_percent=0.7, seed=0):
    wordlemmatizer = WordNetLemmatizer()
    commonwords = stopwords.words('english')

    good_posts = []
    bad_posts = []

    p = Path('subreddits/{0}'.format(subreddit))
    directories = [x for x in p.iterdir() if x.is_dir()]

    weights = []
    for directory in directories:
        for file in directory.iterdir():
            with open(file, 'rb') as f:
                weight = 1
                data = json.load(f)
                if data['score'] >= 10000:
                    weight = 3
                elif data['score'] >= 5000:
                    weight = 1
                elif data['score'] >= 1000:
                    weight = 2
                elif data['score'] <= 250:
                    weight = 2
                elif data['score'] <= 100:
                    weight = 100
                elif data['score'] <= 5:
                    weight = 5

                if data['score'] >= 500:
                    good_posts.append((data['title'], weight))
                else:
                    bad_posts.append((data['title'], weight))

    all_posts = [(title, 'good', weight) for (title, weight) in good_posts]
    all_posts += [(title, 'bad', weight) for (title, weight) in bad_posts]
    class_labels = ['good', 'bad']

    word_counts = {}
    for (title, label, weight) in all_posts:
        word_tokens = [wordlemmatizer.lemmatize(word.lower()) for word in word_tokenize(title)]
        for word in word_tokens:
            if word not in commonwords:
                word_counts[word] = (word_counts.get(word, 0) + 1 * weight)

    sorted_counts = sorted(word_counts.items(), key=operator.itemgetter(1))
    sorted_counts.reverse()

    cleaned_counts = dict(word_counts)
    # for word, count in word_counts.items():
    #     if (count < 5):
    #         del cleaned_counts[word]

    vocabulary = list(cleaned_counts.keys())
    vocab_size = len(vocabulary)

    random.seed(seed)
    random.shuffle(all_posts)

    weights = [weight for (title, label, weight) in all_posts]
    examples = [(feature_extractor(title, cleaned_counts), label, weight) for (title, label, weight) in all_posts]

    train_set_size = int(len(examples) * split_percent)
    train_set = examples[:train_set_size]
    test_set = examples[train_set_size:]

    return (train_set, test_set)

    # print(naiveBayesTest(train_set, test_set))
    # print(naiveBayesTestBag(train_set, test_set, vocabulary, examples, class_labels))

def feature_extractor(title, counts):
    wordlemmatizer = WordNetLemmatizer()

    features = {}
    word_tokens = [wordlemmatizer.lemmatize(word.lower()) for word in word_tokenize(title)]
    for word in word_tokens:
        if word in counts:
            features[word] = True
    return features

# Naive Bayes
def buildProbabilityTable(train):
    # count total number of instances of each label and attribute
    labelCounts = {}
    attrCounts = {}
    attrLabelCounts = {}
    for (example, label, weight) in train:
        labelCounts[label] = labelCounts.get(label, 0) + 1
        count = 0
        for attr in example:
            attrCounts[attr] = attrCounts.get(attr, 0) + 1
            attrLabelCounts[(attr, label)] = attrLabelCounts.get((attr, label), 0) + 1 * weight
        count += 1
        
    # compute unconditional class probabilities
    uncondProbs = {}
    for (l, c) in labelCounts.items():
        uncondProbs[l] = c / len(train)
            
    # compute conditional class|attribute probabilities
    condProbs = {}
    for ((a,l), c) in attrLabelCounts.items():
        condProbs[(l,a)] = c / attrCounts[a] # fraction of messages containing word a which were class l

    return (uncondProbs, condProbs)

def naiveBayesClassify(probs, example):
    (uncondProbs, condProbs) = probs
    guessProbs = {}
    for (l, p) in uncondProbs.items():
        guessProbs[l] = p # we want unconditional * product of conditional probabilities
        for a in example:
            #print("a:",a,'p:',guessProbs[l])
            guessProbs[l] *= condProbs.get((l,a), 0.00001) # note non-zero default; prevents issues with "new" words
    
    guess = max(guessProbs.items(), key=operator.itemgetter(1))[0]
    return guess
    
def naiveBayesTest(train, test):
    # First, we need to train our model
    probs = buildProbabilityTable(train)
    # then, test that model
    correct = 0
    total_good = 0
    good_right = 0
    total_bad = 0
    bad_right = 0
    for (title, label, weight) in test:
        if label == 'good':
            total_good += 1
        elif label == 'bad':
            total_bad += 1

        if label == naiveBayesClassify(probs, title):
            correct += 1
            if label == 'good':
                good_right += 1
            elif label == 'bad':
                bad_right += 1
    
    print('accuracy:', correct / len(test))
    print('Good correct:{0}/{1}'.format(good_right, total_good))
    print('Bad correct:{0}/{1}'.format(bad_right, total_bad))
    return (correct / len(test))