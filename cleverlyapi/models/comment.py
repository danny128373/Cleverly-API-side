from django.db import models
from .profile import Profile
from .post import Post

class Comment(models.Model):
    content = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("Comment")
        verbose_name_plural = ("Comments")
        