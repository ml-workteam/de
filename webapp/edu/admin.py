from django.contrib import admin

from .models import User, Task, Event, Producerlog

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_guest', 'join_date', 'registration_date')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'user', 'target', 'action_id')    

@admin.register(Producerlog)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'ts', 'min_id', 'max_id', 'producer_id', 'status', 'has_errors')      

