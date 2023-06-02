from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    caption_text = models.CharField(blank=True, max_length=64)
    body = models.ImageField(blank=False, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author}, {self.created_at}"
    
    def reply_count(self):
        return Reply.objects.filter(post=self).count()


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    caption_text = models.CharField(blank=True, max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Reply by {self.user.username} on {self.post}"
    
    class Meta:
        ordering = ['-created_at']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def follow(self, user):
        self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User) 