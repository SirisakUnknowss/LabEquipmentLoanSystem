from django.contrib import admin
from .models import EquipmentCart
from import_export.admin import ImportExportModelAdmin


@admin.register(EquipmentCart)
class EquipmentCartAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'user', 'quantity', 'equipment' ]