from django.contrib import admin
from .models import EquipmentCart, Borrowing, Order
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import resources

@admin.register(EquipmentCart)
class EquipmentCartAdmin(ImportExportModelAdmin):

    list_display = [ 'id', 'user', 'quantity', 'equipment' ]

@admin.register(Borrowing)
class BorrowingAdmin(ImportExportModelAdmin):

    list_display = [ 'id', 'user', 'quantity', 'equipment' ]

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):

    list_display = [ 'id', 'user', 'quantity', 'dateBorrowing', 'dateReturn', 'approver', 'status' ]

class OrderModelResource(resources.ModelResource):

    class Meta:
        model = Order

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset

class OrderModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderModelResource