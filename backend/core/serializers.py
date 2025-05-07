from rest_framework import serializers
from .models import Event, Tag
from .models import Bookmark

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all()
    )

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'latitude', 'longitude', 'tags']
        
class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'event', 'created_at']