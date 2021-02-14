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
    join_date = models.DateTimeField(auto_now_add=True)


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

    user_id = models.ForeignKey('User', on_delete = models.CASCADE)
    action_id = models.SmallIntegerField(choices=ACTION_CHOICES, default= 0)
    target_id = models.ForeignKey('Task', on_delete = models.CASCADE)
    time = models.DateTimeField() 


    class Meta:
        ordering = ('time',)


    def __str__(self):
        return str(self.user_id) + "_" + str(self.action_id)    

