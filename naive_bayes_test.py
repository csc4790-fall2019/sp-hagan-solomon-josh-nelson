import json
import math
import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from pathlib import Path

p = Path('subreddits/AskHistorians')
directories = [x for x in p.iterdir() if x.is_dir()]

text_data = []
labels = []

for directory in directories:
    for file in directory.iterdir():
        with open(file) as f:
            data = json.load(f)
            text_data.append(data['title'])
            if data['score'] >= 10:
                labels.append('good')
            else:
                labels.append('bad')

Reddit_Data = {'Title': text_data,'Score': labels}
df = pd.DataFrame(Reddit_Data, columns=['Title', 'Score'])
df = df.reindex(np.random.permutation(df.index))

text_clf = Pipeline([('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', MultinomialNB()),
])

SPLIT_RATIO = 0.6
split_point = math.floor(len(df.index) * SPLIT_RATIO)

train_data = df['Title'][0:split_point]
train_labels = df['Score'][0:split_point]
test_data = df['Title'][split_point:len(text_data)]
test_labels = df['Score'][split_point:len(labels)]

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(train_data)

clf = MultinomialNB().fit(X_train_counts, train_labels)

predicted = clf.predict(count_vect.transform(test_data))

# Output testing
print(np.array(test_labels))
print('---------')
print(predicted)
print(np.mean(predicted == test_labels))

total_good = 0
total_good_right = 0
total_bad = 0
total_bad_right = 0

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

print('Total correct good: {0} / {1}'.format(total_good_right, total_good) +
    ' ({0})'.format(total_good_right / total_good))

print('Total correct bad: {0} / {1}'.format(total_bad_right, total_bad) +
    ' ({0})'.format(total_bad_right / total_bad))