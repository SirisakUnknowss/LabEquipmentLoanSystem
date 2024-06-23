# Django
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Project
from base.variables import STATUS_STYLE
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

FIELDS = ['user__studentID', 'scientificInstrument__name', 'dateBooking', 'startBooking', 'endBooking', 'status', 'createAt', 'approver__studentID',]
class BookingModelResource(resources.ModelResource):

    class Meta:
        model = Booking
        fields = FIELDS

    def dehydrate_status(self, booking):
        return STATUS_STYLE[booking.status]["text"]

    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = Booking.objects.all()
        dataset = super().export(queryset, *args, **kwargs)
        ordered_columns = FIELDS
        new_dataset = dataset.__class__(headers=[ 'รหัสนักศึกษา', 'ชื่อเครื่องมือ', 'วันที่ใช้งาน', 'เวลาเริ่มใช้', 'เวลาสิ้นสุด', 'สถานะ', 'วันที่จอง', 'ผู้อนุมัติ' ])
        for row in dataset.dict:
            new_row = [row[column] for column in ordered_columns]
            new_dataset.append(new_row)
        return new_dataset

@admin.register(Booking)
class BookingAdmin(ImportExportModelAdmin):
    resource_class = BookingModelResource

    list_display    = [ 'id', 'scientificInstrument', 'status' ]
    list_filter     = ['user__studentID', 'status']
    search_fields   = ['user__studentID']

class ScientificInstrumentModelResource(resources.ModelResource):

    class Meta:
        model = ScientificInstrument
        fields = ('name','place','number','detail','annotation','statistics')

    def export(self, queryset=None, *args, **kwargs):
        queryset = super().export(queryset, *args, **kwargs)
        return queryset