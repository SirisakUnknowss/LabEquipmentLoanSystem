from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export import fields, resources
# Project
from base.variables import STATUS_STYLE
from chemicalSubstance.models import ChemicalSubstance, HazardCategory, Withdrawal, Order, ChemicalSubstanceCart

@admin.register(HazardCategory)
class HazardCategoryCartAdmin(ImportExportModelAdmin):

    list_display = [ 'id', 'name' ]

    def get_list_display(self, request):
        return self.list_display + ["thumbnail_preview"]
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True

@admin.register(ChemicalSubstance)
class ChemicalSubstanceAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'name', 'serialNumber', 'catalogNo' ]
    list_filter     = ['name', 'serialNumber', 'hazardCategory', 'ghs']
    search_fields   = ['name', 'serialNumber', 'hazardCategory', 'ghs']

    def get_list_display(self, request):
        return self.list_display + ["thumbnail_preview"]
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True

class ChemicalSubstanceModelResource(resources.ModelResource):

    class Meta:
        model = ChemicalSubstance
        fields = ('name','serialNumber','casNo','place', 'initialQuantity', 'remainingQuantity'
                  , 'unit', 'catalogNo','manufacturer', 'distributor', 'grade','price'
                  , 'buyInDate', 'activateDate','expirationDate', 'hazardCategory'
                  , 'ghs','statistics')
        export_order = fields

    def dehydrate_ghs(self, queryset: ChemicalSubstance):
        return ', '.join([ghs.name for ghs in queryset.ghs.all()])

    def dehydrate_unClass(self, queryset: ChemicalSubstance):
        return ', '.join([unclass.name for unclass in queryset.unClass.all()])

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = ChemicalSubstance.objects.all()
        queryset = queryset.prefetch_related('ghs', 'unClass')
        dataset = super().export(queryset, *args, **kwargs)
        dataset.headers = [
            'Name', 'Serial Number', 'CAS No', 'Place', 'Initial Quantity', 'Remaining Quantity',
            'Unit', 'Catalog Number', 'Manufacturer', 'Distributor', 'Grade', 'Price',
            'Buy-in Date', 'Activate Date', 'Expiration Date', 'Hazard Category',
            'GHS Names', 'Statistics'
        ]
        return dataset

class WithdrawalResource(resources.ModelResource): 
    class Meta:
        model   = Withdrawal
        exclude = ('id', 'user' )

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):

    list_display    = ['id', 'user', 'quantity' ]
    list_filter     = ['user__studentID']
    search_fields   = ['user__studentID']

FIELDS = [ 'user__studentID', 'chemicalSubstance', 'dateWithdraw', 'dateApproved', 'status', 'approver__firstname' ]
class OrderResource(resources.ModelResource):
    chemicalSubstance = fields.Field(
        column_name='chemicalSubstance',
        attribute='chemicalSubstance',
        widget=ManyToManyWidget(Withdrawal, field='chemicalSubstance', separator=', ')
    )
    class Meta:
        model   = Order
        fields  = FIELDS

    def dehydrate_status(self, order):
        return STATUS_STYLE[order.status]["text"]

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = Order.objects.all()
        dataset = super().export(queryset, *args, **kwargs)
        ordered_columns = FIELDS
        new_dataset = dataset.__class__(headers=[ 'รหัสนักศึกษา', 'สารเคมี', 'วันที่เบิก', 'วันที่อนุมัติ', 'สถานะ', 'ผู้อนุมัติ' ])
        for row in dataset.dict:
            new_row = [row[column] for column in ordered_columns]
            new_dataset.append(new_row)
        return new_dataset

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display    = ['id', 'user', 'dateWithdraw', 'dateApproved', 'approver', 'status', ]
    list_filter     = ['user__studentID', 'status']
    search_fields   = ['user__studentID']

@admin.register(ChemicalSubstanceCart)
class ChemicalSubstanceCartAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'user', 'quantity', 'chemicalSubstance' ]
    list_filter     = ['user__studentID']
    search_fields   = ['user__studentID']