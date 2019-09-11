import os
import nltk
import pandas as pd
import time
from pathlib import Path
import re

data_folder = Path("D:\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
raw_data = data_folder / "casual_conversation_top_all.txt";
tokenize_data = data_folder / "casual_conversation_top_all_tokens.txt"
frequency_output = data_folder / "casual_conversation_top_all_title_freq.txt"
with open(raw_data, 'r', encoding='utf-8') as sf:
    data = sf.read()

# https://stackoverflow.com/questions/23142251/is-there-a-way-to-remove-all-characters-except-letters-in-a-string-in-python
alpha_only_data = re.sub(r'([^\s\w]|_)+', '', data)

# Starting timer
start_time = time.time()

data_tokens = nltk.word_tokenize(alpha_only_data)

print(alpha_only_data)

with open(tokenize_data, 'w') as wf:
    tokenize_data.write_text(alpha_only_data)

from nltk.probability import FreqDist

fdist = FreqDist()

for word in data_tokens:
    fdist[word.lower()] += 1

print(fdist)

'''for keys,values in fdist:
    print(keys + ":" + values)'''

for word in fdist:
    print(word)

'''
with open(frequency_output, 'a', encoding='utf-8') as f:
    holderString = fdist.pprint(
    f.write(cop)'''

print("--- %s seconds ---" % (time.time() - start_time))
print("c'est fini")
