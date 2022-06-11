# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    path('register', views.user_register, name='registerApi'),
    path('login', views.user_login, name='loginApi'),
    path('logout', views.user_logout, name='logoutApi'),
    path('update', views.user_edit, name='updateAccoutApi'),
    path('delete', views.delete_account, name='deleteAccount'),
    
]