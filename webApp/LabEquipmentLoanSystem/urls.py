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
    path('register', baseViews.registerPage, name='registerPage'),
    path('export/api/user', baseViews.ExportUserData.as_view(), name='ExportUserData'),
    path('export/api/borrowing', baseViews.ExportBorrowingData.as_view(), name='ExportBorrowingData'),
    path('analysis', baseViews.analysisPage, name='analysisPage'),
    path('user/management', baseViews.userManagementPage, name='userManagementPage'),
    path('user/edit', baseViews.userEditPage, name='userEditPage'),
    path('contact', baseViews.contactPage, name='contactPage'),
    path('account/profile', baseViews.profilePage, name='profilePage'),
    path('api/account/', include('account.urls')),
    #equipment
    path('api/equipment/', include('equipment.urls')),
    path('equipment', baseViews.equipmentLandingPage, name='equipmentLandingPage'),
    path('equipment/add', baseViews.addEquipmentPage, name='addEquipmentPage'),
    path('equipment/list', baseViews.equipmentListPage, name='equipmentListPage'),
    path('equipment/detail', baseViews.detailEquipmentPage, name='detailEquipmentPage'),
    path('equipment/notifications', baseViews.notificationsEquipmentPage, name='notificationsEquipmentPage'),
    path('equipment/borrowing', baseViews.equipmentCartListPage, name='equipmentCartListPage'),
    path('equipment/information', baseViews.informationEquipmentPage, name='informationEquipmentPage'),
    path('equipment/history-borrowing', baseViews.borrowingHistoryPage, name='borrowingHistoryPage'),
    path('export/api/equipments', baseViews.ExportEquipments.as_view(), name='ExportEquipments'),
    #borrowing
    path('api/borrowing/', include('borrowing.urls')),
    path('equipment/borrowing', baseViews.addScientificInstrumentPage, name='addScientificInstrumentPage'),
    #scientific instruments
    path('api/scientificInstrument/', include('scientificInstrument.urls')),
    path('scientificInstrument', baseViews.scientificInstrumentLandingPage, name='scientificInstrumentLandingPage'),
    path('scientificInstrument/calendar', baseViews.scientificInstrumentsCalendarPage, name='scientificInstrumentsCalendarPage'),
    path('scientificInstrument/list', baseViews.scientificInstrumentsListPage, name='scientificInstrumentsListPage'),
    path('scientificInstrument/add', baseViews.addScientificInstrumentPage, name='addScientificInstrumentPage'),
    path('scientificInstrument/information', baseViews.informationBookingPage, name='informationBookingPage'),
    path('scientificInstrument/detail', baseViews.detailScientificInstrumentPage, name='detailScientificInstrumentPage'),
    path('scientificInstrument/notification', baseViews.notificationBookingPage, name='notificationBookingPage'),
    path('scientificInstrument/analysis', baseViews.analysisScientificInstrumentPage, name='analysisScientificInstrumentPage'),
    path('export/api/scientificInstrument', baseViews.ExportScientificInstruments.as_view(), name='ExportScientificInstruments'),
    path('export/api/booking', baseViews.ExportBookingData.as_view(), name='ExportBookingData'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
