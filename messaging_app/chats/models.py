from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    """
        An extension of the Abstract user for valves not defined in django
    """
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=11,blank=True,null=True)
    
    
    
class Conversation(models.Model):
    
    """
        Coversation model that tracks which user are involved in a conversion
    """
    participants = models.ManyToManyField(CustomUser, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """
        Model model containing the sender, converation
    """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

