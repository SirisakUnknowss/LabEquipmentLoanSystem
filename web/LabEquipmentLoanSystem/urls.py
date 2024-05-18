"""web URL Configuration

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
from django.conf import settings
from django.conf.urls import handler404, handler500, handler403, handler400
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
# Project
from base import views as baseViews
from base import equipmentViews
from base import SLViews
from base import CSViews
from base import errorPageView



handler400 = errorPageView.badRequest
handler403 = errorPageView.permissionDenied
handler404 = errorPageView.pageNotFound
handler500 = errorPageView.serverError

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', baseViews.LandingView.as_view(), name='homepage'),
    path('notFound', baseViews.NotFoundPageView.as_view(), name='notFoundPage'),
    path('register', baseViews.SignupView.as_view(), name='registerPage'),
    path('export/api/user', baseViews.ExportUserData.as_view(), name='ExportUserData'),
    path('export/api/borrowing', baseViews.ExportBorrowingData.as_view(), name='ExportBorrowingData'),
    path('user/management', baseViews.UserManagementView.as_view(), name='userManagementPage'),
    path('user/edit', baseViews.UserEditPageView.as_view(), name='userEditPage'),
    path('contact', baseViews.ContactView.as_view(), name='contactPage'),
    path('account/profile', baseViews.ProfileView.as_view(), name='profilePage'),
    path('account/edit', baseViews.EditProfileView.as_view(), name='editProfilePage'),
    path('api/account/', include('account.urls')),
    #equipment
    path('api/equipment/', include('equipment.urls')),
    path('equipment/add', equipmentViews.AddPageView.as_view(), name='addEquipmentPage'),
    path('equipment/edit', equipmentViews.EditPageView.as_view(), name='editEquipmentPage'),
    path('equipment/analysis', equipmentViews.AnalysisView.as_view(), name='analysisPage'),
    path('equipment/list', equipmentViews.ListPageView.as_view(), name='equipmentListPage'),
    path('equipment/detail', equipmentViews.DetailPageView.as_view(), name='detailEquipmentPage'),
    path('equipment/notifications', equipmentViews.NotificationsPageView.as_view(), name='notificationsEquipmentPage'),
    path('equipment/borrowing', equipmentViews.CartListPageView.as_view(), name='equipmentCartListPage'),
    # path('equipment/information', baseViews.InformationEquipmentView.as_view(), name='informationEquipmentPage'),
    path('equipment/history', equipmentViews.BorrowingHistoryView.as_view(), name='borrowingHistoryPage'),
    path('export/api/equipments', baseViews.ExportEquipments.as_view(), name='ExportEquipments'),
    #borrowing
    path('api/borrowing/', include('borrowing.urls')),
    #scientific instruments
    path('api/scientificInstrument/', include('scientificInstrument.urls')),
    path('scientificInstrument/calendar', SLViews.CalendarView.as_view(), name='scientificInstrumentsCalendarPage'),
    path('scientificInstrument/list', SLViews.ListPageView.as_view(), name='scientificInstrumentsListPage'),
    path('scientificInstrument/add', SLViews.AddPageView.as_view(), name='addScientificInstrumentPage'),
    path('scientificInstrument/edit', SLViews.EditPageView.as_view(), name='editScientificInstrumentPage'),
    # path('scientificInstrument/information', SLViews.informationBookingPage, name='informationBookingPage'),
    path('scientificInstrument/detail', SLViews.DetailBookingView.as_view(), name='detailScientificInstrumentPage'),
    path('scientificInstrument/notifications', SLViews.NotificationsBookingView.as_view(), name='notificationBookingPage'),
    path('scientificInstrument/analysis', SLViews.AnalysisPageView.as_view(), name='analysisScientificInstrumentPage'),
    path('export/api/scientificInstrument', baseViews.ExportScientificInstruments.as_view(), name='ExportScientificInstruments'),
    path('export/api/booking', baseViews.ExportBookingData.as_view(), name='ExportBookingData'),
    #chemical Substance
    path('api/chemicalSubstance/', include('chemicalSubstance.urls')),
    path('chemicalSubstance/list', CSViews.ListPageView.as_view(), name='chemicalSubstanceListPage'),
    path('chemicalSubstance/add', CSViews.AddPageView.as_view(), name='chemicalSubstanceAddPage'),
    path('chemicalSubstance/edit', CSViews.EditPageView.as_view(), name='chemicalSubstanceEditPage'),
    path('chemicalSubstance/notifications', CSViews.NotificationsPageView.as_view(), name='chemicalSubstanceNotificationPage'),
    path('chemicalSubstance/history', CSViews.WithdrawHistoryView.as_view(), name='withdrawHistoryPage'),
    path('chemicalSubstance/analysis', CSViews.AnalysisView.as_view(), name='analysisChemicalSubstancePage'),
    path('export/api/chemicalSubstance', baseViews.ExportChemicalSubstances.as_view(), name='ExportChemicalSubstances'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]