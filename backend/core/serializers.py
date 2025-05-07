from rest_framework import serializers
from .models import Event, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)  # nested tags

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'latitude', 'longitude', 'tags']
