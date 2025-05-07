from django.urls import path
from .views import event_list_create, event_detail

urlpatterns = [
    path('events/', event_list_create, name='event_list_create'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
]

