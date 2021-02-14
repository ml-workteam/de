from django.urls import path
from . import views
app_name = 'edu'
urlpatterns = [
    path('events/',
         views.EventListView.as_view(),
         name='event_list'),
    path('events/<pk>/',
         views.EventDetailView.as_view(),
         name='event_detail'),
    path('users/',
         views.UserListView.as_view(),
         name='user_list'),
    path('users/<pk>/',
         views.UserDetailView.as_view(),
         name='user_detail'),     
    path('tasks/',
         views.TaskListView.as_view(),
         name='task_list'),
    path('tasks/<pk>/',
         views.TaskDetailView.as_view(),
         name='task_detail'),     
]