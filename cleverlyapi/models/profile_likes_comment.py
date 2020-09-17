from django.db import models
from .profile import Profile
from .comment import Comment

class ProfileLikesComment(models.Model):
    status = models.CharField(max_length=10)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("profile_likes_comment")
        verbose_name_plural = ("profile_likes_comments")