from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin

# Project
from .models import Account

@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):

    list_display = ['id', 'studentID', 'email', 'firstname', 'lastname', 'gender', 'status']
    fieldsets = (
        ('Account', {'fields': ('studentID', 'password', 'levelclass', 'branch', 'faculty')}),
        ('Personal info', {'fields': ('firstname', 'lastname', 'gender', 'email', 'phone', 'status')}),
    )
    add_fieldsets = (
        ('Account', {
            'classes': ('wide',),
            'fields': ('studentID', 'password', 'levelclass', 'branch', 'faculty')}
        ),
        ('Personal info', {'fields': ('firstname', 'lastname', 'gender', 'email', 'phone', 'status')}),
    )
    search_fields = ['studentID', 'firstname', 'lastname', 'gender', 'levelclass', 'branch', 'faculty', 'status']
    ordering = ['id', 'studentID', 'firstname', 'lastname', 'gender', 'levelclass', 'branch', 'faculty', 'status']
