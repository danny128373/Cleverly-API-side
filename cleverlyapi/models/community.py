from django.db import models
from .profile import Profile

class Community(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=500, default='')
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Community")
        verbose_name_plural = ("Communities")
        