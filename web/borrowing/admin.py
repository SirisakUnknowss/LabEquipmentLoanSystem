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
    list_filter     = ['user__studentID']
    search_fields   = ['id']

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin):

    list_display = [ 'id', 'user', 'quantity', 'dateBorrowing', 'dateReturn', 'approver', 'status' ]
    list_filter     = ['user__studentID', 'approver', 'status']
    search_fields   = ['id']

class OrderModelResource(resources.ModelResource):

    class Meta:
        model = Order
        fields = ('user__studentID','equipment','dateBorrowing','dateApproved','dateReturn','approver__studentID','status')

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset

class OrderModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderModelResource