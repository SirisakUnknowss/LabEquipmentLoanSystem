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
from django.conf import settings
from django.conf.urls.static import static
# Project
from base import views as baseViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', baseViews.homepage, name='homepage'),
    path('register', baseViews.registerpage, name='registerpage'),
    path('notifications', baseViews.notificationspage, name='notifications-forgetten'),
    path('information', baseViews.informationpage, name='information-equipment'),
    path('history-borrowing', baseViews.borrowinghistorypage, name='borrowing-history'),
    path('export/api/user', baseViews.ExportUserData.as_view(), name='ExportUserData'),
    path('export/api/borrowing', baseViews.ExportBorrowingData.as_view(), name='ExportBorrowingData'),
    path('analysis', baseViews.analysispage, name='analysispage'),
    path('user/management', baseViews.usermanagementpage, name='usermanagementpage'),
    path('user/edit', baseViews.usereditpage, name='managepage'),
    path('contactpage', baseViews.contactpage, name='contact-us'),
    path('account/profile', baseViews.profilepage, name='user-profile'),
    path('api/account/', include('account.urls')),
    #equipment
    path('api/equipment/', include('equipment.urls')),
    path('equipment/add', baseViews.addequipmentpage, name='addequipmentpage'),
    path('equipment/list', baseViews.equipmentlistpage, name='equipment-list'),
    path('export/api/equipments', baseViews.ExportEquipments.as_view(), name='ExportEquipments'),
    path('equipment/detail', baseViews.equipmentdetailpage, name='equipment-detail'),
    #borrowing
    path('api/borrowing/', include('borrowing.urls')),
    path('equipment/borrowing', baseViews.equipmentcartlistpage, name='equipmentcart-list'),
    #scientific instruments
    # path('scientificInstruments/calendar', baseViews.scientificinstrumentscalendarpage, name='scientific-instruments-calendar'),
    # path('scientificInstruments/list', baseViews.scientificinstrumentslistpage, name='scientific-instruments-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
