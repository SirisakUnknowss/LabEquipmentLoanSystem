# Django
from django.urls import path
# Project
from . import views

urlpatterns = [
    # path('register', views.register, name='registerApi'),
    path('login', views.user_login, name='loginApi'),
    path('logout', views.user_logout, name='logoutApi'),
]