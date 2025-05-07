from django.urls import path
from .views import event_list_create

urlpatterns = [
    path('events/', event_list_create, name='event_list_create'),
]

