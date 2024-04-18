from django.contrib import admin
from .models import Equipment
from import_export.admin import ImportExportModelAdmin
from import_export import resources


@admin.register(Equipment)
class EquipmentAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'name', 'quantity', 'size', 'unit' ]

    def get_list_display(self, request):
        return self.list_display + ["thumbnail_preview"]
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True

class EquipmentModelResource(resources.ModelResource):

    class Meta:
        model = Equipment
        fields = ('name','quantity','size','unit','brand','statistics')

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset
