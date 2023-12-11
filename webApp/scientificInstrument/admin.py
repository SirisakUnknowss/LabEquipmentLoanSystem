#Django
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
#Project
from scientificInstrument.models import ScientificInstrument, Booking


@admin.register(ScientificInstrument)
class ScientificInstrumentAdmin(ImportExportModelAdmin):

    list_display    = [ 'id', 'name', 'number', 'place' ]

    def get_list_display(self, request):
        return self.list_display + ["thumbnail_preview"]
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail

    thumbnail_preview.short_description = 'Thumbnail'
    thumbnail_preview.allow_tags = True

class BookingModelResource(resources.ModelResource):

    class Meta:
        model = Booking
        fields = ('user__studentID','scientificInstrument__name','createAt', 'dateBooking', 'startBooking','endBooking','approver__studentID','status')
        export_order = ['dateBooking']

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset

@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin):
    resource_class = BookingModelResource

class ScientificInstrumentModelResource(resources.ModelResource):

    class Meta:
        model = ScientificInstrument
        fields = ('name','place','number','detail','annotation','statistics')

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset