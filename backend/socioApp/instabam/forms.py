from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email", "username", "password1", "password2"]

        # widgets = {
        #     'email': forms.TextInput(attrs={'class': 'form-control'}),
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password1': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password2': forms.TextInput(attrs={'class': 'form-control'})
        # }

    
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ["caption_text", "body"]

        widgets = {
            'caption_text': forms.TextInput(attrs={'class': 'form-control'})
        }

