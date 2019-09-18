import os
import nltk
import json
import pandas as pd
import time
from pip._internal.utils import encoding
from main import reddit as reddit

from pathlib import Path
import re

testing_folder = Path('testing')
frequency_folder = Path('frequencies')
with open(testing_folder / 'testing.json', 'r') as file:
    test = json.load(file)


frequency_folder = Path('frequencies')
if not Path(frequency_folder).exists():
    Path(frequency_folder).mkdir()

sentence = test['title']

data_folder = Path("D: =  auth['client_id']\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
raw_data = data_folder / "casual_conversation_top_all.txt";
tokenize_data = data_folder / "casual_conversation_top_all_tokens.txt"
frequency_output = data_folder / "casual_conversation_top_all_title_freq.txt"

with open(raw_data, 'r', encoding='utf-8') as sf:
    data = sf.read()

# https://stackoverflow.com/questions/23142251/is-there-a-way-to-remove-all-characters-except-letters-in-a-string-in-python
line = re.sub('[!@#$,{}]', '', data)
alpha_only_data = re.sub(r'([^\s\w]|_)+', '', data)

# Starting timer
start_time = time.time()

data_tokens = nltk.word_tokenize(alpha_only_data)

print(alpha_only_data)

with open(tokenize_data, 'w', encoding='utf-8') as wf:
    try:
        tokenize_data.write_text(alpha_only_data)
    except:
        print("encoding charmap error")

from nltk.probability import FreqDist

fdist = FreqDist()

for word in data_tokens:
    fdist[word.lower()] += 1

print(fdist)


'''for keys,values in fdist:
    print(keys + ":" + values)'''

for word in fdist:
    print(word)


fdist.pprint()

with open((frequency_folder / 'frequencies.json'), 'w', encoding='utf-8') as file:
    json.dump(frequency_folder, file)


print("--- %s seconds ---" % (time.time() - start_time))
print("c'est fini")

