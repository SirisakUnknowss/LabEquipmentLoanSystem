from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
#Project
from .models import DataWeb

# Register your models here.

@admin.register(DataWeb)
class DataWebAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'linkAssessmentForm', 'fileUserManual' ]
