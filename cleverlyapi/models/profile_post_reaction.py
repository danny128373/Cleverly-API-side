from django.db import models
from .profile import Profile
from .post import Post

class ProfilePostReaction(models.Model):
    status = models.CharField(max_length=10)
    profile = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("profile_post_reaction")
        verbose_name_plural = ("profile_post_reactions")