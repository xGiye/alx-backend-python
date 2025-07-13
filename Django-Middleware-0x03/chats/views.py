# from django.shortcuts import render

# # Create your views here.
# from rest_framework import viewsets, status, filters
# from rest_framework.response import Response
# from .models import Conversation, Message, User
# from .serializers import ConversationSerializer, MessageSerializer

# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['participants__username']

#     def create(self, request, *args, **kwargs):
#         participants = request.data.get('participants')
#         if not participants or len(participants) < 2:
#             return Response({'error': 'A conversation requires at least two participants.'}, status=status.HTTP_400_BAD_REQUEST)
        
#         conversation = Conversation.objects.create()
#         conversation.participants.set(participants)
#         conversation.save()

#         serializer = self.get_serializer(conversation)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['message_body', 'sender__username']

#     def create(self, request, *args, **kwargs):
#         sender = request.data.get('sender')
#         conversation = request.data.get('conversation')
#         message_body = request.data.get('message_body')

#         if not all([sender, conversation, message_body]):
#             return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         message = Message.objects.create(
#             sender_id=sender,
#             conversation_id=conversation,
#             message_body=message_body
#         )

#         serializer = self.get_serializer(message)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# from django.shortcuts import render
# from rest_framework import viewsets, status, filters, serializers  # 👈 serializers added
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Conversation, Message, User
# from .serializers import ConversationSerializer, MessageSerializer

# class ConversationViewSet(viewsets.ModelViewSet):
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['participants__username']

#     def get_queryset(self):
#         # Only return conversations the authenticated user is part of
#         return Conversation.objects.filter(participants=self.request.user)

#     def perform_create(self, serializer):
#         # Automatically include the requesting user as a participant
#         participants = self.request.data.get('participants')
#         if not participants or len(participants) < 2:
#             raise serializers.ValidationError("A conversation requires at least two participants.")
        
#         serializer.save()
#         serializer.instance.participants.set(participants)
#         serializer.instance.participants.add(self.request.user)


# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['message_body', 'sender__username']

#     def get_queryset(self):
#         # Only return messages in conversations the user is a participant of
#         return Message.objects.filter(conversation__participants=self.request.user)

#     def perform_create(self, serializer):
#         conversation_id = self.request.data.get('conversation')
#         if not conversation_id:
#             raise serializers.ValidationError("Conversation is required.")

#         try:
#             conversation = Conversation.objects.get(id=conversation_id)
#         except Conversation.DoesNotExist:
#             raise serializers.ValidationError("Conversation does not exist.")

#         if self.request.user not in conversation.participants.all():
#             raise serializers.ValidationError("You are not a participant of this conversation.")

#         serializer.save(sender=self.request.user, conversation=conversation)


from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation

from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def get_queryset(self):
        # Return only conversations the user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        participants = request.data.get('participants')
        if not participants or len(participants) < 2:
            return Response(
                {'error': 'A conversation requires at least two participants.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    # filter_backends = [filters.SearchFilter]
    
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    
    
    search_fields = ['message_body', 'sender__username']
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Return only messages from conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        sender = request.user
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not conversation_id or not message_body:
            return Response(
                {'error': 'Conversation and message body are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, id=conversation_id)

        if sender not in conversation.participants.all():
            return Response(
                {'error': 'You are not a participant of this conversation.'},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
