from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # The root URL now points to our new homepage view
    path('', views.home_view, name='home'),
    
    # The list of all articles is now at its own URL
    path('articles/', views.post_list, name='post_list'),
    
    # All other URLs remain the same
    path('post/<int:id>', views.post_details, name='post_details'),
    path('post/<int:id>/like', views.like_post, name='like_post'),
    path('post/create', views.post_create, name='post_create'),
    path('post/update/<int:id>', views.post_update, name='post_update'),
    path('post/delete/<int:id>', views.post_delete, name='post_delete'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('chatbot/', views.chatbot_view, name='chatbot'),

    # --- NEW PASSWORD RESET URLS ---
    # 1. Request a password reset
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='user/password_reset_form.html'), 
         name='password_reset'),
    
    # 2. Show a confirmation that the email was sent
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), 
         name='password_reset_done'),
    
    # 3. The link in the email, where the user enters a new password
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    
    # 4. Show a final success message
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), 
         name='password_reset_complete'),
]
