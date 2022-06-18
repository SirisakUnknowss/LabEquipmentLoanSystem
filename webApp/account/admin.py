from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportMixin, ExportMixin

# Project
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = ['id', 'studentID', 'email', 'nameprefix', 'firstname', 'lastname', 'status', 'category']
    fieldsets = (
        ('Account', {'fields': ('user', 'studentID', 'password', 'levelclass', 'branch', 'faculty')}),
        ('Personal info', {'fields': ('nameprefix', 'firstname', 'lastname', 'email', 'phone', 'status', 'category')}),
    )
    add_fieldsets = (
        ('Account', {
            'classes': ('wide',),
            'fields': ('user', 'studentID', 'password', 'levelclass', 'branch', 'faculty')}
        ),
        ('Personal info', {'fields': ('nameprefix', 'firstname', 'lastname', 'email', 'phone', 'status', 'category')}),
    )
    search_fields = ['studentID', 'nameprefix', 'firstname', 'lastname', 'levelclass', 'branch', 'faculty', 'status', 'category']
    ordering = ['id', 'studentID', 'nameprefix', 'firstname', 'lastname', 'levelclass', 'branch', 'faculty', 'status', 'category']
