#Django
from rest_framework.permissions import AllowAny
#Project
from base.views import LabListView, LabAPIGetView
from .serializers import SlzEquipmentInput, SlzEquipment
from .models import Equipment

# Create your views here.
class ListEquipment(LabListView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipment
    permission_classes = [ AllowAny ]

class AddEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes = [ AllowAny ]