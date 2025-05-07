from django.urls import path
from .views import event_list_create, event_detail
from .views import event_list_create, event_detail, bookmark_list_create, bookmark_delete

urlpatterns = [
    path('events/', event_list_create, name='event_list_create'),
    path('events/<int:pk>/', event_detail, name='event_detail'),
    path('bookmarks/', bookmark_list_create, name='bookmark_list_create'),
    path('bookmarks/<int:pk>/', bookmark_delete, name='bookmark_delete'),

]

