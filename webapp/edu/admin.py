from django.contrib import admin

from .models import User, Task, Event

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_guest')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('time', 'user_id', 'target_id', 'action_id')    

