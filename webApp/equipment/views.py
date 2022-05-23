#Django
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
#Project
from base.views import LabListView, LabAPIGetView
from .serializers import SlzEquipmentInput, SlzEquipment
from .models import Equipment, getClassPath

# Create your views here.
class ListEquipment(LabListView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipment
    permission_classes = [ AllowAny ]

class AddEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        equipment               = self.perform_create(serializerInput)
        serializerOutput        = SlzEquipment(equipment)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('equipment-list'))
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        equipment = Equipment(
            name        = validated.get("name"),
            quantity    = validated.get("quantity"),
            size        = validated.get("size"),
            unit        = validated.get("unit"),
        )
        equipment.save()
        if not(self.request.FILES['upload']):
            return equipment
        upload      = self.request.FILES['upload']
        fss         = FileSystemStorage()
        name        = getClassPath(equipment, validated.get("name"))
        file        = fss.save(name, upload)
        file_url    = fss.url(file)
        equipment.image = file_url
        equipment.save()
        return equipment