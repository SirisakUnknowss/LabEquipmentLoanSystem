#Django
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import F
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
#Project
from account.admin import AccountResource
from account.models import Account
from base.functions import uploadImage, downloadFile, getDataFile, writeFileExcel, exportAccountData
from base.permissions import IsAdminAccount
from base.views import LabListView, LabAPIGetView, LabAPIView
from borrowing.admin import OrderModelResource
from borrowing.models import Order, Borrowing
from equipment.serializers import SlzEquipmentInput, SlzEquipment
from equipment.models import Equipment, getClassPath
from settings.base import MEDIA_ROOT

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

class ExportUserEquipments(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        fileName = f"UserEquipmentsData"
        queryset = Account.objects.filter(accountOrder__isnull=False).distinct()
        return exportAccountData(queryset, fileName)

    def writeFile(self):
        userFileDir = "UserEquipmentsData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Account.objects.filter(accountOrder__isnull=False).distinct()
        fileName = f"UserEquipmentsData"
        
        xlsxFile = getDataFile(dirPath, fileName, AccountResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportOrderEquipments(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        filePath, fileName = self.writeFile()
        return downloadFile(filePath, fileName)

    def writeFile(self):
        userFileDir = "OrderEquipmentsData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Order.objects.all()
        fileName = f"OrderEquipmentsData"
        
        xlsxFile = getDataFile(dirPath, fileName, OrderModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportUsesEquipments(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        if bool(request.GET and request.GET['id']):
            id = request.GET['id']
            return self.getWithID(id)
        return self.getAllItems()

    def getWithID(self, id: str):
        queryset = Equipment.objects.filter(id=id)
        if not queryset.exists(): return
        equipment   = queryset[0]
        fileName    = f'Uses_{equipment.name}'
        header      = { 'date': 'วันที่ยืม - คืน', 'studentID': 'รหัสนักศึกษา', 'name': 'ชื่อ', 'quantity': 'ปริมาณที่ยืม - คืน' }
        orders = Order.objects.all()
        equipmentList = []
        for order in orders:
            for item in order.equipment.all():
                borrowing: Borrowing = item
                key     = borrowing.equipment.pk
                if key != equipment.pk: continue
                equipmentList.append({
                    'date': order.dateBorrowing,
                    'studentID': f'{order.user.studentID}',
                    'name': f'{order.user.firstname} {order.user.lastname}',
                    'quantity': f'{borrowing.quantity} {borrowing.equipment.unit}'
                })
        print(equipmentList)
        return writeFileExcel(equipmentList, header, fileName)
            
    def getAllItems(self):
        fileName    = 'Uses_Equipments'
        header      = { 'number': 'ลำดับ', 'name': 'ชื่ออุปกรณ์วิทยาศาสตร์', 'size': 'ขนาด', 'time': 'จำนวนทั้งหมด' }
        orders      = Order.objects.all()
        equipmentList = {}
        for order in orders:
            for item in order.equipment.all():
                borrowing: Borrowing = item
                key = borrowing.equipment.pk
                if key in equipmentList:
                    equipmentList[key]['quantity'] += borrowing.quantity
                else:
                    equipmentList[key] = {
                        'quantity': borrowing.quantity,
                        'unit': borrowing.equipment.unit
                    }
        queryset    = Equipment.objects.all().order_by('-statistics').filter(statistics__gte=1)
        equipments  = []
        number      = 1
        for data in queryset:
            if data.pk in equipmentList:
                quantity    = equipmentList[data.pk]['quantity']
                unit        = equipmentList[data.pk]['unit']
                equipments.append({
                    'number': number,
                    'name': data.name,
                    'size': f'{data.size} {unit}',
                    'time': quantity,
                })
                number += 1
        return writeFileExcel(equipments, header, fileName)