from django.db import models
from .profile import Profile
from .community import Community

class Post(models.Model):
    content = models.CharField(max_length=500)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    community = models.ForeignKey(Community, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name = ("Post")
        verbose_name_plural = ("Posts")
        