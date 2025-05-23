# Django
from django.shortcuts import get_object_or_404

# DRF Core
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Local Models
from .models import Event, Bookmark, Tag

# Local Serializers
from .serializers import EventSerializer, BookmarkSerializer, TagSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(created_by=request.user)
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if event.created_by != request.user:
            return Response({'detail': 'Not authorized to update this event'}, status=status.HTTP_403_FORBIDDEN)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if event.created_by != request.user:
            return Response({'detail': 'Not authorized to delete this event'}, status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def bookmark_list_create(request):
    if request.method == 'GET':
        bookmarks = Bookmark.objects.filter(user=request.user)
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def bookmark_delete(request, pk):
    bookmark = get_object_or_404(Bookmark, pk=pk, user=request.user)
    bookmark.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmark_toggle(request):
    event_id = request.data.get('event')
    if not event_id:
        return Response({"detail": "Missing event ID."}, status=status.HTTP_400_BAD_REQUEST)

    event = get_object_or_404(Event, pk=event_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, event=event)

    if not created:
        bookmark.delete()
        return Response({"detail": "Bookmark removed."}, status=status.HTTP_200_OK)
    
    return Response({"detail": "Bookmark added."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def tag_list(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)