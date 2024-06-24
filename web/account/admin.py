# Python
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Django
from django.contrib import admin

# Project
from .models import Account

class AccountResource(resources.ModelResource): 
    class Meta:
        model = Account
        exclude = ('id', 'user', 'password', 'prefix', 'levelClass', 'branch', 'faculty', 'image')
        export_order = ('studentID', 'email', 'firstname', 'lastname', 'phone', 'category', 'categoryOther', 'status')

@admin.register(Account)
class AccountAdmin(ImportExportModelAdmin):

    list_display = ['id', 'studentID', 'email', 'prefix', 'firstname', 'lastname', 'status', 'categoryTH', 'branchTH', ]
    fieldsets = (
        ('Account', {'fields': ('user', 'studentID', 'password', 'levelClass', 'branch', 'faculty')}),
        ('Personal info', {'fields': ('prefix', 'firstname', 'lastname', 'email', 'phone', 'status', 'category', 'categoryOther', 'image')}),
    )
    add_fieldsets = (
        ('Account', {
            'classes': ('wide',),
            'fields': ('user', 'studentID', 'password', 'levelClass', 'branch', 'faculty')}
        ),
        ('Personal info', {'fields': ('prefix', 'firstname', 'lastname', 'email', 'phone', 'status', 'category')}),
    )
    search_fields = ['studentID', 'prefix', 'firstname', 'lastname', 'levelClass', 'branch', 'faculty', 'status', 'category']
    ordering = ['id', 'studentID', 'prefix', 'firstname', 'lastname', 'levelClass', 'branch', 'faculty', 'status', 'category']
    list_filter = ['category', 'status']
