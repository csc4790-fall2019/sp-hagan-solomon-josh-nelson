import praw
import json
import utils
import clfs
from scraper import scrape
from sklearn.model_selection import train_test_split

def main(runs):
	with open('auth.json', 'r') as file:
	    auth = json.load(file)

	reddit = praw.Reddit(client_id=auth['client_id'],
	                     client_secret=auth['client_secret'],
	                     username=auth['username'],
	                     password=auth['password'],
	                     user_agent='This is a test.')

	#scrape('AskReddit', reddit)
	data = utils.get_data('AskReddit')

	test_title = input('Enter a title: ')
	prediction = clfs.predict_title(data, test_title, 10)
	print('Prediction for "{0}": {1}'.format(test_title, prediction))

	success_pct, failure_pct, avg_pct = clfs.get_total_percentages(data, runs)
	print('Success Posts %: {0}'.format(success_pct))
	print('Failure Posts %: {0}'.format(failure_pct))
	print('Average Posts %: {0}'.format(avg_pct))

main(20)