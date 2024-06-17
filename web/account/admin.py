# Python
from import_export import resources
# Django
from django.contrib import admin

# Project
from .models import Account

class AccountResource(resources.ModelResource): 
    class Meta:
        model = Account
        exclude = ('id', 'user', 'password', 'nameprefix', 'levelclass', 'branch', 'faculty', 'image')
        export_order = ('studentID', 'email', 'firstname', 'lastname', 'phone', 'category', 'categoryOther', 'status')

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = ['id', 'studentID', 'email', 'nameprefix', 'firstname', 'lastname', 'status', 'categoryTH', 'branchTH', ]
    fieldsets = (
        ('Account', {'fields': ('user', 'studentID', 'password', 'levelclass', 'branch', 'faculty')}),
        ('Personal info', {'fields': ('nameprefix', 'firstname', 'lastname', 'email', 'phone', 'status', 'category', 'categoryOther', 'image')}),
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
    list_filter = ['category', 'status']
