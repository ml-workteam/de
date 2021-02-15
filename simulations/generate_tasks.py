import requests
import json
from random import sample, randint
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

if __name__ == "__main__":

    verbs = ['Solve', 'Make programm', 'Find solution', 'Prove']
    nouns = ['task', 'problem', 'minimum', 'maximum', 'TKS', 'MVP', 'T4', 'A1', 'B3', 'C5', 'L6']

    url = 'http://127.0.0.1:8000/api/tasks/'

    tasks = list()

    for verb in verbs:
        for noun in nouns:
            tasks.append(" ".join([verb, noun]))

    for task in tasks:
        row = dict()
        row['name'] = task
        r = requests.post(url, data=row)
        logging.info("{0} - {1}".format(str(r.status_code), str(r.reason)))

    logging.info("Generated {0} tasks".format(len(tasks)))  
