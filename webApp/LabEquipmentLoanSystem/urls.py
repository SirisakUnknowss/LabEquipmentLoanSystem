"""webApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.contrib import admin
from django.urls import path, include
# Project
from base import views as baseViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', baseViews.homepage, name='homepage'),
    path('register', baseViews.registerpage, name='registerpage'),
    path('notifications', baseViews.notificationspage, name='notifications-forgetten'),
    path('information', baseViews.informationpage, name='information-equipment'),
    path('equipment-list', baseViews.equipmentlistpage, name='equipment-list'),
    path('history-borrowing', baseViews.borrowinghistorypage, name='borrowing-history'),
    path('contactpage', baseViews.contactpage, name='contact-us'),
    path('account/profile', baseViews.profilepage, name='user-profile'),
    path('api/account/', include('account.urls')),
    #equipment
    path('api/equipment/', include('equipment.urls')),
    path('equipment/add', baseViews.addequipmentpage, name='addequipmentpage'),
]
