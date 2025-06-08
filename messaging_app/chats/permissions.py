# from rest_framework import permissions

# class IsParticipantOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user in obj.participants.all()
from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to participants of a conversation.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # For Message objects
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False
