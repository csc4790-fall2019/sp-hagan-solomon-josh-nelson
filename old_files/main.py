import praw
import json
import utils
import clfs
from zipf import populate_freq_dist_stop_list
from scraper import scrape
from clfs import test
from sklearn.model_selection import train_test_split

def main(title_runs, total_percent_runs):
    with open('auth.json', 'r') as file:
        auth = json.load(file)

    reddit = praw.Reddit(client_id=auth['client_id'],
                         client_secret=auth['client_secret'],
                         username=auth['username'],
                         password=auth['password'],
                         user_agent='This is a test.')

    #scrape('AskReddit', reddit)
    #populate_freq_dist_stop_list('this is a title', 'AskReddit')
    data = utils.get_data('AskReddit')
    data = utils.get_data('askreddit')

    test_title = input('Enter a title: ')
    prediction = clfs.predict_title(data, test_title, title_runs)
    print('Prediction for "{0}": {1}'.format(test_title, prediction))

    success_pct, failure_pct, avg_pct = clfs.get_total_percentages(data, total_percent_runs)
    print('Viral Post Correctness: {0}'.format(success_pct))
    print('Not Viral Post Correctness: {0}'.format(failure_pct))
    print('Average Correctness: {0}'.format(avg_pct))


    sp = round(success_pct * 100, 1)
    fp = round(failure_pct * 100, 1)
    ap = round(avg_pct * 100, 1)
    
    clfs.mat_plot_test_accuracy(sp, fp, ap)

    return prediction[0]

main(3, 1)

