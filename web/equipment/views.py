#Django
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import F
from rest_framework.exceptions import ValidationError
#Project
from base.functions import uploadImage
from base.views import LabListView, LabAPIGetView
from .serializers import SlzEquipmentInput, SlzEquipment
from .models import Equipment, getClassPath

# Create your views here.
class ListEquipment(LabListView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipment
    permission_classes  = [ AllowAny ]

class AddEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        equipment               = self.perform_create(serializerInput)
        serializerOutput        = SlzEquipment(equipment)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('equipmentListPage'))
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        equipment = Equipment.objects.filter(name=validated.get("name"), size=validated.get("size"), brand=validated.get("brand"))
        if equipment.exists():
            equipment.update(quantity=F('quantity') + validated.get("quantity"))
            return equipment.first()
        else:
            unit = validated.get("unit")
            if unit == 'Other_Other':
                unit = self.request.POST['unitOther']
            equipment = Equipment(
                name        = validated.get("name"),
                quantity    = validated.get("quantity"),
                size        = validated.get("size"),
                unit        = unit,
            )
            equipment.save()
            if not(self.request.FILES.get('upload', False)):
                return equipment
            upload  = self.request.FILES['upload']
            name    = getClassPath(equipment, validated.get("name"))
            uploadImage(name, upload, equipment)
            return equipment
        
class RemoveEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        Equipment.objects.filter(id=request.POST["equipment"]).delete()
        return redirect(reverse('equipmentListPage'))

class EditEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        equipment = Equipment.objects.filter(id=request.POST["equipment"])
        if not equipment.exists():
            return redirect(reverse('equipmentListPage'))
            
        unit = request.POST["unit"]
        if unit == 'Other_Other':
            unit = self.request.POST['unitOther']
        equipment.update(
            name=request.POST["name"],
            size=request.POST["size"],
            quantity=request.POST["quantity"],
            unit=unit,
            )
        if not(request.FILES.get('upload', False)):
            return redirect(reverse('equipmentListPage'))
        equipment   = equipment[0]
        upload      = self.request.FILES['upload']
        name        = getClassPath(equipment, request.POST["name"])
        uploadImage(name, upload, equipment)
        return redirect(reverse('equipmentListPage'))