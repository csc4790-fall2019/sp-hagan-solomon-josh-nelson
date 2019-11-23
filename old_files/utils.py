import json
import numpy as np
import pandas as pd
from pathlib import Path

def get_data(subreddit):
    p = Path('subreddits/{0}'.format(subreddit_name))
    files = [x for x in p.iterdir() if x.is_file()]

    text_data = []
    labels = []
    weights = []

    for file in files:
        with open(file) as f:
            data = json.load(f)
            text_data.append(data['title'])
            if data['score'] >= 2000:
                labels.append('1')
            else:
                labels.append('0')

    Reddit_Data = {'Title': text_data,'Rating': labels}
    df = pd.DataFrame(Reddit_Data, columns=['Title', 'Rating'])
    df = df.reindex(np.random.permutation(df.index))

    return df