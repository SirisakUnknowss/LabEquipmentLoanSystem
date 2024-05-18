from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import resources
from .models import ChemicalSubstance, HazardCategory, Withdrawal, Order

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

    list_display = [ 'id', 'name', 'serialNumber', 'catalogNo' ]

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
        model = Withdrawal
        exclude = ('id', 'user' )

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'quantity' ]

class OrderResource(resources.ModelResource): 
    class Meta:
        model = Order
        exclude = ('id', 'user', 'approver' )
        export_order = ('id', 'user', 'dateWithdraw', 'dateApproved', 'status',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'dateWithdraw', 'dateApproved', 'approver', 'status', ]