import os
import nltk
import json
import pandas as pd
import time
from pathlib import Path
import re

frequency_folder = Path('frequencies')
if not Path(frequency_folder).exists():
    Path(frequency_folder).mkdir()

testing_folder = Path('testing')
frequency_folder = Path('frequencies')
with open(testing_folder / 'testing.json', 'r') as file:
    test = json.load(file)





# Starting timer
start_time = time.time()







print("--- %s seconds ---" % (time.time() - start_time))
print("c'est fini")