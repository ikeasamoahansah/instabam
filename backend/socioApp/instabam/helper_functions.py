import os
from .models import *

def get_and_del(request):
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            os.remove(post.body.path)