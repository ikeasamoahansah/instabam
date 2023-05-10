from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout_view, name="logout"),
    path('post_cont', views.post_content, name="post"),
    path('profile/u/<int:id>', views.profile, name="profile")
]