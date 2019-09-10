import os
import nltk
from pathlib import Path

data_folder = Path("D:\Senior Project Holder all\Reddit Proj\Text Data\Testing Purposes");
raw_data = data_folder / "casual_conversation_top_all.txt";
tokenize_data = data_folder / "casual_conversation_top_all_tokens.txt"

with open(raw_data, 'r', encoding='utf-8') as sf:
    data = sf.read()

print(type(data))

data_tokens = nltk.word_tokenize(data)



with open(tokenize_data, 'w') as wf:
    tokenize_data.write_text(data)


'''
if you comment out everything from line 9 to 20 and replace it with this you should print out 
a tokenized tester_string

tester_string = "hello everyone how are you"
ret_string = nltk.word_tokenize(tester_string)
print(ret_string)
'''