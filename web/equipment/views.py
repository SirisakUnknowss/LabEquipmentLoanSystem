#Django
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import F
from rest_framework import status
from rest_framework.response import Response
#Project
from base.functions import uploadImage
from base.permissions import IsAdminAccount
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
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        try:
            serializerInput = self.get_serializer(data=request.data)
            if not serializerInput.is_valid():
                self.response["error"] = next(iter(serializerInput.errors.values()))[0]
                return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializerInput)
            self.response["result"] = '/equipment/add'
            return Response(self.response)
        except Exception as ex:
            self.response["error"] = f"{ex}"
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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

class EditEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    serializer_class    = SlzEquipmentInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        try:
            equipment = Equipment.objects.get(id=request.POST["dataID"])
            self.update(equipment)
            self.response["result"] = '/equipment/list'
            return Response(self.response)
        except Equipment.DoesNotExist:
                self.response["result"] = '/equipment/edit'
                return Response(self.response, status=status.HTTP_404_NOT_FOUND)

    def update(self, equipment: Equipment) -> Equipment:
        data = self.request.POST
        unit = data.get("unit")
        if unit == 'Other_Other':
            unit = data.get('unitOther')
        equipment.name      = data.get("name")
        equipment.size      = data.get("size")
        equipment.quantity  = data.get("quantity")
        equipment.unit      = unit
        equipment.save()
        if not(self.request.FILES.get('upload', False)):
            return equipment
        upload  = self.request.FILES['upload']
        name    = getClassPath(equipment, data.get("name"))
        uploadImage(name, upload, equipment)
        return equipment

class RemoveEquipment(LabAPIGetView):
    queryset            = Equipment.objects.all()
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        try:
            Equipment.objects.get(id=request.POST["dataID"]).delete()
            self.response["result"] = 'ลบข้อมูลเรียบร้อย'
            return Response(self.response)
        except Equipment.DoesNotExist:
            self.response["error"] = 'ไม่พบข้อมูล'
            return Response(self.response, status=status.HTTP_404_NOT_FOUND)