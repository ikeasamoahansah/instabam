from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(UserProfile)
admin.site.register(LikePost)
admin.site.register(FollowersCount)
