from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout_view, name="logout"),
    path('post_cont', views.post_content, name="post"),
    path('search/', views.search, name='search'),
    path('profile/u/<int:my_id>', views.profile, name="profile"),
    path('profile/u/update_user', views.update_user, name="update_user" ),
    path('post/<uuid:post_id>/', views.view_post, name='view_post'),
    path('post/<uuid:post_id>/reply/', views.reply, name='reply'),

    path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='registration/reset_password.html'), 
         name="reset_password"),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='registration/reset_password_sent.html'), 
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='registration/reset_password_confirm.html'), 
         name="password_reset_confirm"),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/reset_password_complete.html'), 
         name="password_reset_complete")
]