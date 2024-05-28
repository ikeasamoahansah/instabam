from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User 
from .models import Post, UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]


class UpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["bio", "profileimg", "location"]

    
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["caption_text", "body"]


class EditUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"] 