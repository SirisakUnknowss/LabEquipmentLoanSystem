from django.contrib import admin
from .models import ChemicalSubstance, HazardCategory
from import_export.admin import ImportExportModelAdmin, ExportMixin
from import_export import resources

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