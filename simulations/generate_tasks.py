import requests
import json
from random import sample, randint
from datetime import datetime, timedelta

verbs = ['Решить', 'Найти', 'Определить', 'Доказать']
nouns = ['теорему', 'задачу', 'минимум', 'максимум', 'ТКС', 'МПВ', 'Т4', 'А1']

url = 'http://127.0.0.1:8000/api/tasks/'

tasks = list()

for verb in verbs:
    for noun in nouns:
        tasks.append(" ".join([verb, noun]))

for task in tasks:
    row = dict()
    row['name'] = task
    r = requests.post(url, data=row)
    print(r.status_code, r.reason)      
