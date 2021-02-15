import sqlite3
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from random import randint
from config import conf
from datetime import datetime
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

class Producer:


    def __init__(self, last_id = None, id = None):

        if id is None:
            self.id = str(randint(1, 10000))
        else:
            self.id = id    

        self.last_id = last_id # None will start from last recorded value
        self.query = conf['query']
        self.kafka = KafkaProducer(
                                    bootstrap_servers=['localhost:9092'], 
                                    value_serializer=lambda m: json.dumps(m).encode('utf8'),
                                    acks = 'all', retries = 999,
                                    retry_backoff_ms = 1000,
                                    request_timeout_ms = 1000 * 60 * 5,
                                    max_in_flight_requests_per_connection = 1
                                    )


    def make_query(self):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        
        conn = sqlite3.connect(conf['db_path']) 
            #detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES
        conn.row_factory = dict_factory
        cursor = conn.cursor()

        if self.last_id is None:
            # берем последний занятый max_id
            get_last_query = conf['get_last_query']
            lastid = cursor.execute(get_last_query).fetchall()
            if len(lastid) > 0:
                last_id = lastid[0]['max_id']
            else:
                last_id = 0    

        else:
            last_id = self.last_id
            self.last_id = None # теперь будем стартовать с продолжения

        query = self.query.format(last_id)
        try:
            res = cursor.execute(query)
            rows = res.fetchall()
            logging.info("Fetched {0} rows.".format(len(rows)))

        except Exception as e:
            loggin.info("Error: {0}".format(str(e)))
            rows = None

        # в случае удачной выборки (rows is not null && len(rows) > 0) запишем в работу новую строку
        # 
        if (rows is not None) and (len(rows) > 0):

            min_id = rows[0]['event_id']
            max_id = rows[-1]['event_id']

            ins_query = conf['insert_producerlog_query']
            try:
                cursor.execute(ins_query, {'min_id': min_id, 'max_id': max_id, 
                                                'producer_id': self.id, 'ts': datetime.now(),
                                                'status': 0,
                                                'has_errors': 0
                                                })  

                self.lastrowid = cursor.lastrowid
                cursor.execute("COMMIT")

            except Exception as e:
                logging.info("Insert Processorlog error {0}".format(str(e)))  
        else:
            rows = None        

        conn.close()
        return rows
    
    
    def update_producerlog(self):
        
        conn = sqlite3.connect(conf['db_path'])
        try:
            cursor = conn.cursor()
            cursor.execute("update edu_producerlog set status = 1 where id = :id", {'id': self.lastrowid})
            cursor.execute("commit")
        except Exception as e:
            logging.info("Update error: {0}".format(str(e)))

        conn.close()

    
    def render(self):

        def on_send_success(record_metadata):
            logging.info("Topic: {0} Partition: {1}  Offset: {2}".format(record_metadata.topic, record_metadata.partition, record_metadata.offset))

        def on_send_error(excp):
            logging.info("I am an errback".format(str(excp)))
            # обработка ошибки отправки сообщения в очередь
            # например - скинуть в лог ошибок в базу

        res = self.make_query()

        if (res is not None) and (len(res) > 0):
            # push to kafka
            for row in res:
                self.kafka.send('events', row).add_callback(on_send_success).add_errback(on_send_error)
            logging.info("Everything send async. Waiting for tickets.")     
            self.kafka.flush()
            logging.info("All messages has been sent.")
            self.update_producerlog()
            logging.info("Producer log status updated. Waiting for events ...")

        else:
            logging.info("No events. Waiting for events ...")
    

if __name__ == "__main__":

    producer = Producer(id='uno')
    
    while True:
        res = producer.render()
        time.sleep(60 * 5) # 5 min

    
    producer.kafka.close()
    