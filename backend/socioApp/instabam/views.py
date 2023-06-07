from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


import os
from .models import *
from .forms import *

# Create your views here.

def get_and_del(request):
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            os.remove(post.body.path)

@login_required(login_url='/login')
def home(request):
    get_and_del(request)
    return render(request, "instabam/home.html", {"posts": Post.objects.all().order_by('-updated_at')})

def logout_view(request):
    logout(request)
    return redirect('login')

def login(request):
    if request.method == "GET":
        return render(request, "registration/login.html")
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/home')
        else:
            return render(request, "registration/login.html", {
                "msg": "Invalid login credentials"
            })
    else:
        return HttpResponse('<h1>Failed attempt to login</h1>')


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {"form":form})


@login_required(login_url='/login')
def post_content(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()
    return render(request, 'instabam/post.html', {"form":form})

@login_required(login_url='/login')
def profile(request, my_id):
    
    user_to_follow = User.objects.get(id=my_id)
    profile = UserProfile.objects.get(user=user_to_follow)
    get_and_del(request)

    if request.method == "POST":
        # current_user_profile = request.user.userprofile

        action = request.POST["follow"]

        if action == "unfollow":
            # current_user_profile.follows.remove(profile)
            unfollow_user(request, my_id)
        elif action == "follow":
            # current_user_profile.follows.add(profile)
            follow_user(request, my_id)

        # current_user_profile.save()
    
    return render(request, 'instabam/profile.html', {
        "profile": profile,
        "posts": Post.objects.all().order_by('-updated_at')
    })


@login_required(login_url='/login')
def update_user(request):
        
    current_user = User.objects.get(id=request.user.id)

    if request.method == "POST":
        form = RegisterForm(request.POST or None, instance=current_user)
        if form.is_valid():
            form.save()
            auth_login(request, current_user)
            return redirect(f'/profile/u/{request.user.id}')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/update_user.html', {
        "form": form
    })

@login_required(login_url='/login')
@require_POST
def reply(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        caption_text = request.POST.get('caption_text')
        reply = Reply(user=request.user, post=post, caption_text=caption_text)
        reply.save()
        return redirect(f"/post/{post_id}")
    else:
        return render(HttpResponse(
            'None'
        ))

@login_required(login_url='/login')
def view_post(request, post_id):
    post= get_object_or_404(Post, id=post_id)
    reply_count = post.reply_count()
    replies = Reply.objects.filter(post=post)
    context = {
        'post': post,
        'reply_count': reply_count,
        'replies': replies,
    }
    return render(request, 'instabam/view_post.html', context)

@login_required(login_url='/login')
def search(request):
    query = request.GET.get('q')

    # Perform search for users and posts
    users = User.objects.filter(username__icontains=query)
    posts = Post.objects.filter(caption_text__icontains=query)

    context = {
        'query': query,
        'users': users,
        'posts': posts,
    }

    return render(request, 'instabam/search.html', context)

@login_required(login_url='/login')
def follow_user(request, user_id):
    # Get the UserProfile instance of the current user
    current_user_profile = request.user.userprofile

    # Get the UserProfile instance of the user to be followed
    user_to_follow = get_object_or_404(UserProfile, user=user_id)

    # Add the user_to_follow to the followers of the current_user_profile
    current_user_profile.follow(user_to_follow.user)
    current_user_profile.save()


    return redirect(f'profile/u/{user_id}')

@login_required(login_url='/login')
def unfollow_user(request, user_id):
    # Get the UserProfile instance of the current user
    current_user_profile = request.user.userprofile

    # Get the UserProfile instance of the user to be unfollowed
    user_to_unfollow = get_object_or_404(UserProfile, pk=user_id)

    # Remove the user_to_unfollow from the followers of the current_user_profile
    current_user_profile.unfollow(user_to_unfollow.user)
    current_user_profile.save()


    return redirect(f'profile/u/{user_id}')
