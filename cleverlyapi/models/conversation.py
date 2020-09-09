from django.db import models
from .profile import Profile

class Conversation(models.Model):
    
    profile1 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='profile1')
    profile2 = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='profile2')

    class Meta:
        verbose_name = ("Conversation")
        verbose_name_plural = ("Conversations")