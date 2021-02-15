import requests
import json
from random import sample, randint
from datetime import datetime, timedelta
import time
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s')

class User():

    def __init__(self, data, activity = 10):
        self.data = data
        self.activity = activity
        self.user_id = data['id']
        self.last_action = 2
        self.last_task = None
        self.next_action_count = randint(1, self.activity)


    def take_task(self, stage):
        task = sample(stage.tasks, 1)[0]
        logging.info(str(self) + ' take task ' + str(task))
        return task


    def take_action(self, stage):
            
        if self.last_action == 2:
            self.last_task = self.take_task(stage)
            self.last_action = 0
        else:
            self.last_action += 1

        row = dict()    
        row['user'] = self.user_id
        row['target'] = self.last_task.id()
        row['action_id'] = self.last_action
        row['time'] = stage.epoch_time
        
        r = requests.post(stage.events_url, data=row)       
        logging.info(str(self) + ' take action ' + str(self.last_action) + ' on ' + str(self.last_task) + ' ' + str(r.status_code))


    def update_counter(self):
        if self.next_action_count <= 0:
            self.next_action_count = randint(1, self.activity)    
        else:    
            self.next_action_count -= 1    


    def render(self, stage):
        self.update_counter()
        if self.next_action_count == 0:
            self.take_action(stage)


    def __str__(self):
        return self.data['name']


class Task():

    def __init__(self, data):
        self.data = data
        self.task_id = data['id']

    def __str__(self):
        return self.data['name']

    def id(self):
        return self.task_id    
    

class Stage():

    def __init__(self, tasks_url, users_url, events_url, start_dt = datetime.now(), 
                minutes_per_epoch = 1, realtime = False, realtime_delay = 0.1,
                epoch_delay = 0):
        """
        tasks_url = "http://127.0.0.1/api/tasks/
        users_url = "http://127.0.0.1/api/users/
        """
        self.realtime = realtime
        self.realtime_delay = realtime_delay
        self.epoch_delay = epoch_delay

        self.events_url = events_url

        self.epoch_started = start_dt
        self.minutes_per_epoch = minutes_per_epoch
        self.epoch_time = self.epoch_started

        self.tasks = list()
        tasks = requests.get(tasks_url).json()
        for task in tasks:
            self.tasks.append(Task(task))

        users = requests.get(users_url).json()
        self.users = list()
        for user in users:
            self.users.append(User(user))


    def render(self):

        if self.realtime == True:
            self.epoch_time = datetime.now()
            time.sleep(self.realtime_delay)
        else:
            self.epoch_time = self.epoch_time + timedelta(minutes=self.minutes_per_epoch)
            time.sleep(self.epoch_delay)

        for user in self.users:
            user.render(self)
    

    def make_simulation(self, n=100):
        for i in range(n):
            stage.render()


    def __str__(self):
        return "Simulation Stage started " + str(self.epoch_started)


if __name__ == "__main__":

    stage = Stage(
                "http://127.0.0.1:8000/api/tasks/", 
                "http://127.0.0.1:8000/api/users/", 
                "http://127.0.0.1:8000/api/events/", 
                minutes_per_epoch = 4 * 60,
                epoch_delay = 1
                )


    stage.make_simulation(n=1000)

