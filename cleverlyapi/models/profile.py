from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.CharField(max_length=500)
    about = models.CharField(max_length=255)
    likes = models.IntegerField()

    class Meta:
        verbose_name = ("Profile")
        verbose_name_plural = ("Profiles")