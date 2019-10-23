import json
import numpy as np
import pandas as pd
from pathlib import Path

# STOPWORDS = set(stopwords.words('english'))
STOPWORDS = ['the', 'it', 'a', 'an', 'was', 'were', 'had', 'is', 'have', 'are']

def get_data(subreddit_name):
    p = Path('subreddits/{0}'.format(subreddit_name))
    directories = [x for x in p.iterdir() if x.is_dir()]

    text_data = []
    labels = []
    weights = []

    counter = 0
    for directory in directories:
        for file in directory.iterdir():
            with open(file) as f:
                data = json.load(f)
                text_data.append(data['title'])
                
                if data['score'] >= 500:
                    labels.append('good')
                else:
                    labels.append('bad')


    Reddit_Data = {'Title': text_data,'Rating': labels}
    df = pd.DataFrame(Reddit_Data, columns=['Title', 'Rating'])
    def clean_text(text):
        text = ' '.join(word for word in text.split() if word not in STOPWORDS)
        return text
    df['Title'] = df['Title'].apply(clean_text)
    df = df.reindex(np.random.permutation(df.index))
    return df