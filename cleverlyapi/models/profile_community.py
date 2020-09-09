from django.db import models
from .profile import Profile
from .community import Community

class ProfileCommunity(models.Model):

  """"Creates join table for the many to many realtionship between Profile and Community"""

  profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
  community = models.ForeignKey(Community, on_delete=models.CASCADE)

  class Meta:
    verbose_name = ("profile_community")
    verbose_name_plural = ("profile_communities")
