# Python
from datetime import datetime
# Django
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
#Project
from account.models import Account
from base.permissions import IsAdminAccount
from base.views import LabAPIGetView, LabAPIView
from borrowing.functions import updateStatusOrder, updateApprover, returnEquipments, borrowingAgain
from borrowing.models import Borrowing, EquipmentCart, Order
from borrowing.serializers import (SlzEquipmentCartInput, SlzEquipmentCart, SlzApprovalInput, SlzCancelInput,
                                   SlzReturnInput, SlzConfirmReturnInput, SlzBorrowingAgainInput)
from equipment.models import Equipment

class AddItemForBorrowingApi(LabAPIGetView):
    queryset            = EquipmentCart.objects.all()
    serializer_class    = SlzEquipmentCartInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request, *args, **kwargs):
        account                 = request.user.account
        serializerInput         = self.get_serializer(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return redirect(reverse('equipmentListPage'))
        equipment               = self.perform_create(serializerInput, account)
        serializerOutput        = SlzEquipmentCart(equipment)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('equipmentListPage'))
    
    def perform_create(self, serializer, account):
        validated = serializer.validated_data
        equipmentCart = EquipmentCart.objects.filter(user=account, equipment=validated.get("equipment"))
        if equipmentCart.exists():
            equipmentCart.update(quantity=F('quantity') + validated.get("quantity"))
            return equipmentCart
        equipmentCart = EquipmentCart(
            user        = account,
            equipment   = validated.get("equipment"),
            quantity    = validated.get("quantity"),
            )
        equipmentCart.save()
        return equipmentCart

class RemoveItemForBorrowingApi(LabAPIGetView):
    queryset            = EquipmentCart.objects.all()
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        account = request.user.account
        idCart  = request.data['itemID']
        EquipmentCart.objects.filter(id=idCart, user=account).delete()
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class ConfirmBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        account     = request.user.account
        equipments  = EquipmentCart.objects.filter(user=account)
        if not equipments.exists():
            self.response["error"] = "ไม่มีรายการในตะกร้า"
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        order = Order.objects.create(user=account)
        for item in equipments:
            equipment = Equipment.objects.get(id=item.equipment.id)
            if equipment.quantity < item.quantity:
                self.response["error"] = "รายการคงเหลือไม่เพียงพอ"
                return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            equipment.quantity -= item.quantity
            equipment.save()
            borrowing = Borrowing.objects.create(user=account, equipment=item.equipment, quantity=item.quantity)
            order.equipment.add(borrowing)
        equipments.delete()
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class ApprovalBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
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
        updateApprover(self.order, self.request.user.account)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class CancelBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzCancelInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzCancelInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order   = serializerInput.validated_data['orderID']
        updateStatusOrder(self.order, Order.STATUS.CANCELED)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class RemoveBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        order       = Order.objects.filter(id=orderID, user=account)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.delete()
        return redirect(reverse('borrowingHistoryPage'))

class ReturnEquipmentsApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzReturnInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        data = request.data.copy()
        data.update({'account': request.user.account.pk})
        serializerInput = SlzReturnInput(data=data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order = serializerInput.validated_data['orderID']
        updateStatusOrder(self.order, Order.STATUS.RETURNED)
        self.order.dateReturn   = datetime.now()
        self.order.save(update_fields=["dateReturn"])
        self.response["result"] = 'Update Completed.'
        return Response(self.response)
    
class BorrowingAgainApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzBorrowingAgainInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzBorrowingAgainInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order = serializerInput.validated_data['orderID']
        borrowingAgain(self.order)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class ConfirmReturnApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzConfirmReturnInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzConfirmReturnInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order = serializerInput.validated_data['orderID']
        returnEquipments(self.order)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)