# Python
from csv import DictWriter
from datetime import datetime
import pandas, os
# Django
from django.db.models import F
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
# Project
from account.admin import AccountResource
from account.models import Account
from base.functions import convertToFloat, checkTextBlank, download_file, getDataFile, convertCSVToXLSX
from base.permissions import IsAdminAccount
from base.views import LabAPIView
from chemicalSubstance.admin import OrderResource
from chemicalSubstance.functions import updateHazard, updateImage, updateStatusOrder, cancelOrder
from chemicalSubstance.models import ChemicalSubstance, Order, Withdrawal, ChemicalSubstanceCart
from chemicalSubstance.serializers import (SlzChemicalSubstanceInput, SlzChemicalSubstanceOutput, SlzOrderOutput, 
                                           SlzApprovalInput, SlzCancelInput, SlzChemicalSubstanceCartInput)
from settings.base import MEDIA_ROOT

class AddChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstanceInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request: Request, *args, **kwargs):
        try:
            checkList               = request.data.getlist(request.data['hazardCategory'])
            serializerInput         = SlzChemicalSubstanceInput(data=request.data)
            if not serializerInput.is_valid():
                self.response["error"] = next(iter(serializerInput.errors.values()))[0]
                return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
            chemicalSubstance       = self.perform_create(serializerInput.validated_data, checkList)
            self.response["result"] = '/chemicalSubstance/list'
            return Response(self.response)
        except Exception as ex:
            print("AddChemicalSubstance == " + ex)
            self.response["error"] = f"{ex}"
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, validated: dict, checkList: list):
        chemicalSubstance = ChemicalSubstance(
            name                = validated.get("name"),
            serialNumber        = validated.get("serialNumber"),
            casNo               = validated.get("casNo"),
            place               = validated.get("place"),
            initialQuantity     = validated.get("initialQuantity"),
            remainingQuantity   = validated.get("remainingQuantity"),
            unit                = validated.get("unit"),
            catalogNo           = validated.get("catalogNo"),
            manufacturer        = validated.get("manufacturer"),
            distributor         = validated.get("distributor"),
            grade               = validated.get("grade"),
            price               = convertToFloat(validated.get("price")),
            hazardCategory      = validated.get("hazardCategory"),
            buyInDate           = validated.get("buyInDate"),
            activateDate        = validated.get("activateDate"),
            expirationDate      = validated.get("expirationDate"),
        )
        chemicalSubstance.save()
        chemicalSubstance = updateHazard(chemicalSubstance, checkList)
        chemicalSubstance = updateImage(chemicalSubstance, validated.get('name'), self.request.FILES)
        return chemicalSubstance

class EditChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstanceOutput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request: Request, *args, **kwargs):
        self.chemicalSubstances = ChemicalSubstance.objects.filter(id=request.POST["dataID"])
        if not self.chemicalSubstances.exists():
            self.response["result"] = '/chemicalSubstance/edit'
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        chemicalSubstance = self.chemicalSubstances.first()
        name = self.request.POST.get('name')
        if name != self.chemicalSubstances.first().name:
            try:
                chemicalSubstance = ChemicalSubstance.objects.get(name=name)
                self.response["result"] = '/chemicalSubstance/edit'
                return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except ChemicalSubstance.DoesNotExist:
                pass
        chemicalSubstance = self.update(chemicalSubstance)
        checkList = self.request.POST.getlist(self.request.POST.get('hazardCategory'))
        chemicalSubstance = updateHazard(chemicalSubstance, checkList)
        self.response["result"] = '/chemicalSubstance/list'
        return Response(self.response)

    def update(self, cs: ChemicalSubstance) -> ChemicalSubstance:
        data                    = self.request.POST
        name                    = checkTextBlank(data.get("name"))
        cs.name                 = name
        cs.serialNumber         = checkTextBlank(data.get("serialNumber"))
        cs.casNo                = checkTextBlank(data.get("casNo"))
        cs.place                = checkTextBlank(data.get("place"))
        cs.initialQuantity      = convertToFloat(data.get("initialQuantity"))
        cs.remainingQuantity    = convertToFloat(data.get("remainingQuantity"))
        cs.unit                 = checkTextBlank(data.get("unit"))
        cs.catalogNo            = checkTextBlank(data.get("catalogNo"))
        cs.manufacturer         = checkTextBlank(data.get("manufacturer"))
        cs.distributor          = checkTextBlank(data.get("distributor"))
        cs.grade                = checkTextBlank(data.get("grade"))
        cs.price                = convertToFloat(data.get("price"))
        cs.hazardCategory       = checkTextBlank(data.get("hazardCategory"))
        cs.buyInDate            = checkTextBlank(data.get("buyInDate"))
        cs.activateDate         = checkTextBlank(data.get("activateDate"))
        cs.expirationDate       = checkTextBlank(data.get("expirationDate"))
        cs.save()
        cs = updateImage(cs, name, self.request.FILES)
        return cs

class ApprovalChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzApprovalInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzApprovalInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order   = serializerInput.validated_data['orderID']
        statusStr: str      = serializerInput.validated_data['status']
        updateStatusOrder(self.order, statusStr)
        self.updateApprover()
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

    def updateApprover(self):
        account: Account = self.request.user.account
        self.order.approver = account
        self.order.dateApproved = datetime.now()
        self.order.save(update_fields=["approver", "dateApproved"])

class CancelChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzCancelInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzCancelInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order   = serializerInput.validated_data['orderID']
        cancelOrder(self.order)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class ConfirmWithdrawalApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzOrderOutput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        self.account    = request.user.account
        self.orders     = ChemicalSubstanceCart.objects.all()
        self.orders     = self.validate()
        self.createOrder()
        self.response["result"] = "Save Complete!"
        return Response(self.response)

    def validate(self):
        self.orderValidate = []
        for order in self.orders:
            try:
                chemicalSubstance = ChemicalSubstance.objects.get(id=order.chemicalSubstance.pk)
                if chemicalSubstance.remainingQuantity < order.quantity:
                    raise ValidationError('ปริมาณสารเคมีที่เบิกมีไม่เพียงพอ')
                self.orderValidate.append(order)
            except ChemicalSubstance.DoesNotExist:
                raise ValidationError('ไม่พบสารเคมี')
        return self.orderValidate

    def createOrder(self):
        order = Order.objects.create(user=self.account)
        for chemical in self.orders:
            chemicalSubstance = ChemicalSubstance.objects.get(id=chemical.chemicalSubstance.pk)
            chemicalSubstance.remainingQuantity -= chemical.quantity
            chemicalSubstance.save(update_fields=["remainingQuantity"])
            withdrawal = Withdrawal.objects.create(user=self.account, chemicalSubstance=chemicalSubstance, quantity=chemical.quantity)
            order.chemicalSubstance.add(withdrawal)
            chemical.delete()
        order.save()
        return order

class AddToCartView(LabAPIView):
    queryset            = ChemicalSubstanceCart.objects.all()
    serializer_class    = SlzChemicalSubstanceCartInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        try:
            account                 = request.user.account
            serializerInput         = SlzChemicalSubstanceCartInput(data=request.data)
            serializerInput.is_valid(raise_exception=True)
            if not serializerInput.is_valid():
                self.response["error"] = next(iter(serializerInput.errors.values()))[0]
                return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializerInput.validated_data, account)
            self.response["result"] = 'Add Completed.'
            return Response(self.response)
        except Exception as ex:
            print("=============================")
            print(str(ex))
            print("=============================")
            self.response["error"] = "something went wrong."
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
    
    def perform_create(self, validated: dict, account: Account):
        print(validated.get("id"))
        cart = ChemicalSubstanceCart.objects.filter(user=account, chemicalSubstance=validated.get("id"))
        if cart.exists():
            cart.update(quantity=F('quantity') + validated.get("quantity"))
            return cart
        cart = ChemicalSubstanceCart(
            user                = account,
            chemicalSubstance   = validated.get("id"),
            quantity            = validated.get("quantity"),
            )
        cart.save()
        return cart

class RemoveFromCartView(LabAPIView):
    queryset            = ChemicalSubstanceCart.objects.all()
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        account = request.user.account
        idCart  = request.data['cartID']
        ChemicalSubstanceCart.objects.filter(id=idCart, user=account).delete()
        self.response["result"] = 'Delete Completed.'
        return Response(self.response)

class ExportUserChemicalSubstances(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        filePath, fileName = self.writeFile()
        return download_file(filePath, fileName)

    def writeFile(self):
        userFileDir = "UserChemicalSubstancesData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Account.objects.filter(userOrderWithdraw__isnull=False).distinct()
        fileName = f"UserChemicalSubstancesData"
        
        xlsxFile = getDataFile(dirPath, fileName, AccountResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportOrderChemicalSubstances(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        filePath, fileName = self.writeFile()
        return download_file(filePath, fileName)

    def writeFile(self):
        userFileDir = "OrderChemicalSubstancesData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Order.objects.all()
        fileName = f"OrderChemicalSubstancesData"
        
        xlsxFile = getDataFile(dirPath, fileName, OrderResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportUsesChemicalSubstances(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        if bool(request.GET and request.GET['serialNumber']):
            serialNumber = request.GET['serialNumber']
            return self.getWithSerialNumber(serialNumber)
        return self.getAllItems()

    def getWithSerialNumber(self, serialNumber: str):
        queryset = ChemicalSubstance.objects.filter(serialNumber=serialNumber)
        if not queryset.exists(): return
        chemicalSubstance = queryset[0]
        fileName    = f'Uses_{chemicalSubstance.name}'
        header      = { 'date': 'วันที่เบิก', 'studentID': 'รหัสนักศึกษา', 'name': 'ชื่อ', 'quantity': 'ปริมาณที่เบิกใช้' }
        orders = Order.objects.filter(status=Order.STATUS.APPROVED)
        chemicalList = []
        for order in orders:
            for withdraw in order.chemicalSubstance.all():
                key     = str(withdraw.chemicalSubstance.serialNumber)
                if key != chemicalSubstance.serialNumber: continue
                chemicalList.append({
                    'date': order.dateWithdraw,
                    'studentID': f'{order.user.studentID}',
                    'name': f'{order.user.firstname} {order.user.lastname}',
                    'quantity': f'{withdraw.quantity} {withdraw.chemicalSubstance.unit}'
                })
        return self.writeFileExcel(chemicalList, header, fileName)
            
    def getAllItems(self):
        fileName    = 'Uses_ChemicalSubstances'
        header      = { 'serialNumber': 'รหัส', 'name': 'ชื่อ', 'time': 'จำนวนครั้ง', 'quantity': 'ปริมาณทั้งหมดที่เบิกใช้' }
        orders      = Order.objects.filter(status=Order.STATUS.APPROVED)
        chemicalList = {}
        for order in orders:
            for withdraw in order.chemicalSubstance.all():
                key = str(withdraw.chemicalSubstance.serialNumber)
                if key in chemicalList:
                    chemicalList[key]['quantity'] += withdraw.quantity
                else:
                    chemicalList[key] = {
                        'quantity': withdraw.quantity,
                        'unit': withdraw.chemicalSubstance.unit
                    }
        queryset    = ChemicalSubstance.objects.all().order_by('-statistics').filter(statistics__gt=1)
        chemicals   = []
        for data in queryset:
            serialNumber = str(data.serialNumber)
            if serialNumber in chemicalList:
                quantity    = chemicalList[serialNumber]['quantity']
                unit        = chemicalList[serialNumber]['unit']
                chemicals.append({
                    'serialNumber': serialNumber,
                    'name': data.name,
                    'time': data.statistics,
                    'quantity': f'{quantity} {unit}'
                })
        return self.writeFileExcel(chemicals, header, fileName)

    def writeFileExcel(self, dataList: list, header: dict, fileName: str):
        csvPath = f'{fileName}.csv'
        excelPath = f'{fileName}.xlsx'
        with open(csvPath, 'w', newline='', encoding='utf-8') as outfile:
            writer = DictWriter(outfile, fieldnames=header.keys())
            writer.writerow(header)
            writer.writerows(dataList)
        convertCSVToXLSX(csvPath, excelPath)
        return download_file(excelPath, excelPath)