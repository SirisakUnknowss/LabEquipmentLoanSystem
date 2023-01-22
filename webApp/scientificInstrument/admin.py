#Django
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
#Project
from scientificInstrument.models import ScientificInstrument


@admin.register(ScientificInstrument)
class ScientificInstrumenttAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'name', 'number', 'place' ]

    def get_list_display(self, request):
        return self.list_display + ["thumbnail_preview"]
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True