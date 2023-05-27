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
    return render(request, "instabam/home.html", 
    {
        "posts": Post.objects.all().order_by('-updated_at'),
        "reposts": RePost.objects.all()
    })

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
    
    profile = User.objects.get(id=my_id)
    get_and_del(request)
    
    return render(request, 'instabam/profile.html', {
        "profile": profile,
        "posts": Post.objects.all().order_by('-updated_at'),
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
def repost(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    caption_text = request.POST.get('caption_text')
    repost, created = RePost.objects.get_or_create(user=request.user, post=post, caption_text=caption_text)
    if created:
        repost.save()
    return redirect("/home")

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
    retweet_count = post.retweet_count()
    replies = Reply.objects.filter(post=post)
    context = {
        'post': post,
        'retweet_count': retweet_count,
        'replies': replies,
    }
    return render(request, 'instabam/view_post.html', context)