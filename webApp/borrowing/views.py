from django.shortcuts import render
#Project
from base.views import LabListView, LabAPIGetView

# Create your views here.

class AddItemForBorrowingApi(LabAPIGetView):
    # queryset            = Equipment.objects.all()
    # serializer_class    = SlzEquipmentInput
    # permission_classes = [ AllowAny ]
    def get(self, request, *args, **kwargs):
        return render(request, 'pages/notifications_page.html')
