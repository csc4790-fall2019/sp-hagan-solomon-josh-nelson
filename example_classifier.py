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
                data = json.load(f)
                if data['score'] >= 200:
                    good_posts.append(data['title'])
                else:
                    bad_posts.append(data['title'])

                if data['score'] >= 10000:
                    weights.append(5)
                elif data['score'] >= 5000:
                    weights.append(3)
                elif data['score'] >= 1000:
                    weights.append(2)
                else:
                    weights.append(1)

    all_posts = [(email, 'good') for email in good_posts]
    all_posts += [(email, 'bad') for email in bad_posts]
    class_labels = ['good', 'bad']

    word_counts = {}
    count = 0
    for (title, label) in all_posts:
        word_tokens = [wordlemmatizer.lemmatize(word.lower()) for word in word_tokenize(title)]
        for word in word_tokens:
            if word not in commonwords:
                word_counts[word] = (word_counts.get(word, 0) + 1) * weights[count]
        count += 1

    sorted_counts = sorted(word_counts.items(), key=operator.itemgetter(1))
    sorted_counts.reverse()

    cleaned_counts = dict(word_counts)
    for word, count in word_counts.items():
        if (count < 5):
            del cleaned_counts[word]

    vocabulary = list(cleaned_counts.keys())
    vocab_size = len(vocabulary)

    examples = [(feature_extractor(title, cleaned_counts), label) for (title, label) in all_posts]

    train_set_size = int(len(examples) * split_percent)
    random.seed(seed)
    random.shuffle(examples)
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
    for (example, label) in train:
        labelCounts[label] = labelCounts.get(label, 0) + 1
        for attr in example:
            attrCounts[attr] = attrCounts.get(attr, 0) + 1
            attrLabelCounts[(attr, label)] = attrLabelCounts.get((attr, label), 0) + 1
        
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
    for (mail, label) in test:
        if label == 'good':
            total_good += 1
        elif label == 'bad':
            total_bad += 1

        if label == naiveBayesClassify(probs, mail):
            correct += 1
            if label == 'good':
                good_right += 1
            elif label == 'bad':
                bad_right += 1
    
    print('accuracy:', correct / len(test))
    print('Good correct:{0}/{1}'.format(good_right, total_good))
    print('Bad correct:{0}/{1}'.format(bad_right, total_bad))

# Naive Bayes Bag
def buildProbabilityTableBag(train, vocabulary, examples, class_labels):
    # count total number of instances of each label and attribute
    labelCounts = {}
    attrCounts = {}
    attrLabelCounts = {}
    for (example, label) in train:
        labelCounts[label] = labelCounts.get(label, 0) + 1
        for word in example:
            attrCounts[(word, 1)] = attrCounts.get((word, 1), 0) + 1
            attrLabelCounts[((word, 1), label)] = attrLabelCounts.get(((word, 1), label), 0) + 1
    
    for word in vocabulary:
        attrCounts[(word, 0)] = len(examples) - attrCounts.get((word, 1), 0.0001)
        for label in class_labels:
            attrLabelCounts[((word, 0), label)] = 1 - attrLabelCounts.get(((word, 1), label), 0.0001)
        
    # compute unconditional class probabilities
    uncondProbs = {}
    for (l, c) in labelCounts.items():
        uncondProbs[l] = c / len(train)
            
    # compute conditional class|attribute probabilities
    condProbs = {}
    for ((a,l), c) in attrLabelCounts.items():
        condProbs[(l,a)] = c / attrCounts[a] # fraction of messages containing word a which were class l
    
    return (uncondProbs, condProbs)

def naiveBayesClassifyBag(probs, example, vocabulary):
    (uncondProbs, condProbs) = probs
    guessProbs = {}
    for (l, p) in uncondProbs.items():
        guessProbs[l] = p # we want unconditional * product of conditional probabilities
        for word in vocabulary:
            #print("a:",a,'p:',guessProbs[l])
            if word in example:
                guessProbs[l] *= condProbs.get((l,(word, 1)), 0.00001) # note non-zero default; prevents issues with "new" words
            else:
                guessProbs[l] *= condProbs.get((l,(word, 0)), 0.00001)                                      

    
    guess = max(guessProbs.items(), key=operator.itemgetter(1))[0]
    return guess

def naiveBayesTestBag(train, test, vocabulary, examples, class_labels):
    # First, we need to train our model
    probs = buildProbabilityTableBag(train, vocabulary, examples, class_labels)
    # then, test that model
    correct = 0
    total_good = 0
    good_right = 0
    total_bad = 0
    bad_right = 0
    for (mail, label) in test:
        if label == 'good':
            total_good += 1
        elif label == 'bad':
            total_bad += 1

        if label == naiveBayesClassifyBag(probs, mail, vocabulary):
            correct += 1
            if label == 'good':
                good_right += 1
            elif label == 'bad':
                bad_right += 1
    
    
    print('accuracy:', correct / len(test))
    print('Good correct:{0}/{1}'.format(good_right, total_good))
    print('Bad correct:{0}/{1}'.format(bad_right, total_bad))