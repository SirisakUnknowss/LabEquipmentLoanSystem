from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export.widgets import ManyToManyWidget
from import_export import fields, resources
# Project
from base.variables import STATUS_STYLE
from borrowing.models import EquipmentCart, Borrowing, Order

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

FIELDS = [ 'user__studentID','equipment','dateBorrowing','dateApproved','dateReturn','approver__firstname','status' ]
class OrderModelResource(resources.ModelResource):
    equipment = fields.Field(
        column_name='equipment',
        attribute='equipment',
        widget=ManyToManyWidget(Borrowing, field='equipment', separator=', ')
    )

    class Meta:
        model = Order
        fields = FIELDS

    def dehydrate_status(self, order):
        return STATUS_STYLE[order.status]["text"]

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = Order.objects.all()
        dataset = super().export(queryset, *args, **kwargs)
        ordered_columns = FIELDS
        new_dataset = dataset.__class__(headers=[ 'รหัสนักศึกษา', 'ชื่ออุปกรณ์', 'วันที่ยืม', 'วันที่อนุมัติ', 'วันที่คืน', 'ผู้อนุมัติ', 'สถานะ' ])
        for row in dataset.dict:
            new_row = [row[column] for column in ordered_columns]
            new_dataset.append(new_row)
        return new_dataset

class OrderModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderModelResource