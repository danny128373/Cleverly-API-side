from django.db import models
from .profile import Profile
from .conversation import Conversation

class Message(models.Model):
    content = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Message")
        verbose_name_plural = ("Messages")
        