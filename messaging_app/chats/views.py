from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response({'error': 'A conversation requires at least two participants.'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__username']

    def create(self, request, *args, **kwargs):
        sender = request.data.get('sender')
        conversation = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not all([sender, conversation, message_body]):
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            sender_id=sender,
            conversation_id=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
