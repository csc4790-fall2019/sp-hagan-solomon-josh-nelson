import re
import json
import praw;
import pandas as pd;
import numpy as np;
from pathlib import Path
import time



testing_folder = Path('testing')

with open('testing.json', 'r') as file:
    auth = json.load(file)

