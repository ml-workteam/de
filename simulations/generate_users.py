import requests
import json
from random import sample, randint
from datetime import datetime, timedelta
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')

if __name__ == "__main__":

    logins = ['alex', 'john', 'mike', 'nadya', 'sasha', 'peter', 'fox', 'cat', 'dog']
    domains = ['@mail.ru', '@yahoo.com', '@hotmail.com', '@yandex.ru', '@gmail.com', '@ya.ru', '@list.ru']
    fnames = ['Nadya', 'Anya', 'Julia', 'Sasha', 'Alex', 'Alexey', 'Dan', 'Andy', 'Ira', 'Nomi', 'Elka']
    lnames = ['Marchewka', 'Polenka', 'Kozalko', 'Sarowsky', 'Ishkov']

    url = 'http://127.0.0.1:8000/api/users/'


    emails = list()
    names = list()

    for login in logins:
        for domain in domains:
            emails.append(login + domain)

    for fname in fnames:
        for lname in lnames:
            names.append(" ".join([fname, lname]))


    for email in emails:
        row = dict()
        row['name'] = sample(names, 1)[0]
        row['email'] = email
        row['is_guest'] = sample([0,1], 1)[0]
        if row['is_guest'] == 1:
            row['registration_date'] = datetime(1970,1,1,0,0,0)
        else:
            row['registration_date'] = datetime.now()    
        row['join_date'] = datetime.now()
        
        r = requests.post(url, data=row)
        logging.info("{0} - {1}".format(str(r.status_code), str(r.reason)))

    logging.info("Generated {0} users".format(len(emails)))    



