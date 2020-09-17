from django.db import models
from .profile import Profile
from .post import Post

class Comment(models.Model):
    content = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")
        