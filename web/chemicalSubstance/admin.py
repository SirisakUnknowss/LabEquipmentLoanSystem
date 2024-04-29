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