from django.db import models
from .profile import Profile
from .community import Community

class Relationship(models.Model):

  friender = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='friender')
  friendee = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='friendee')
  status = models.CharField(max_length=20)

  class Meta:
    verbose_name = ("relationship")
    verbose_name_plural = ("relationships")
