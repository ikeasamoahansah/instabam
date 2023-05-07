from django.shortcuts import render
from django.contrib.auth import logout
from .models import *

# Create your views here.
def home(request):
    return render(request, "instabam/home.html", {
        "posts": Post.objects.all()
    })

def logout_view(request):
    logout(request)