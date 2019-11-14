import json
import numpy as np
import pandas as pd
from pathlib import Path

# STOPWORDS = set(stopwords.words('english'))
STOPWORDS = ['the', 'it', 'a', 'an', 'was', 'were', 'had', 'is', 'have', 'are']

def get_data(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    files = [x for x in p.iterdir() if x.is_file()]

    text_data = []
    labels = []
    weights = []

    counter = 0

    good = 0
    medium_high = 0
    medium_low = 0
    bad = 0
    for file in files:
        with open(file) as f:
            data = json.load(f)
            text_data.append(data['title'])
            if data['score'] >= 2000:
                good += 1
                labels.append('1')
            # elif data['score'] >= 1000 and data['score'] < 5000:
            #     medium_high += 1
            #     labels.append('2')
            # elif data['score'] >= 100 and data['score'] < 1000:
            #     medium_low += 1
            #     labels.append('1')
            else:
                bad += 1
                labels.append('0')
    print(good)
    print(medium_high)
    print(medium_low)
    print(bad)


    Reddit_Data = {'Title': text_data,'Rating': labels}
    df = pd.DataFrame(Reddit_Data, columns=['Title', 'Rating'])
    def clean_text(text):
        text = ' '.join(word for word in text.split() if word not in STOPWORDS)
        return text
    df['Title'] = df['Title'].apply(clean_text)
    df = df.reindex(np.random.permutation(df.index))
    return df