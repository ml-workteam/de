from django.urls import path
from . import views
app_name = 'edu'

urlpatterns = [
    # ...
    path('api/', include('edu.api.urls', namespace='api')),
]
