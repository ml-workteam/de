from django.db import models
from django.utils import timezone
import datetime

class User(models.Model):

    GUEST_CHOICES = (
        (0, 'Guest'),
        (1, 'Registered')
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    is_guest = models.BooleanField()
    registration_date = models.DateTimeField(default=datetime.datetime(1970,1,1,0,0,0))
    join_date = models.DateTimeField(default=datetime.datetime.now)


    class Meta:
        ordering = ('join_date',)


    def __str__(self):
        return self.name    


class Task(models.Model):
     
    name = models.CharField(max_length=255)


    def __str__(self):
         return self.name


class Event(models.Model):

    ACTION_CHOICES = (
        (0, 'увидеть задачу'),
        (1, 'сделать сабмит решения'), 
        (2, 'решить задачу'),
    )

    user = models.ForeignKey('User', on_delete = models.CASCADE)
    action_id = models.SmallIntegerField(choices=ACTION_CHOICES, default= 0)
    target = models.ForeignKey('Task', on_delete = models.CASCADE)
    time = models.DateTimeField() 


    class Meta:
        ordering = ('time',)


    def __str__(self):
        return str(self.user_id) + "_" + str(self.action_id)    


class Producerlog(models.Model):

    # {min_id = ..., max_id = .., ts, producer_id, status = 0|1, has_errors = 0|1}

    min_id = models.IntegerField()
    max_id = models.IntegerField()
    ts = models.DateTimeField(auto_now=True)
    producer_id = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    has_errors = models.BooleanField(default=False)

    class Meta:
        ordering = ('min_id',)

    def __str__(self):
        return "Producer " + str(self.producer_id) + " " + str(self.min_id) 



