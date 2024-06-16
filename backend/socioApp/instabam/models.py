from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .helper_model import BaseModel
import uuid

# TODO: Custom user class to enable users get profiles

class Post(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption_text = models.CharField(blank=True, max_length=64)
    body = models.ImageField(blank=False, upload_to="images/")
    
    def __str__(self):
        return f"{self.author}, {self.created_at}"
    
    def reply_count(self):
        return Reply.objects.filter(post=self).count()
    
    def like_count(self):
        return LikePost.objects.filter(post=self).count()


class Reply(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    caption_text = models.CharField(blank=True, max_length=64)

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post}"
    

class LikePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Liked by {self.user.username}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images/', default='blank-profile-picture.jpg')
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username


class FollowersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)