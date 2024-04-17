# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('register', views.user_register, name='registerApi'),
    path('login', views.LoginView.as_view(), name='loginApi'),
    path('logout', views.user_logout, name='logoutApi'),
    path('update', views.user_edit, name='updateAccoutApi'),
    path('delete', views.delete_account, name='deleteAccount'),
    
]