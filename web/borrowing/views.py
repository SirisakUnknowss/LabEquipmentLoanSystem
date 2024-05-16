# Python
from datetime import datetime, timedelta
# Django
from django.db.models import F
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import AllowAny
#Project
from base.views import LabAPIGetView, LabAPIView
from equipment.models import Equipment
from account.models import Account
from .models import Borrowing, EquipmentCart, Order
from .serializers import SlzEquipmentCartInput, SlzEquipmentCart

# Create your views here.

class AddItemForBorrowingApi(LabAPIGetView):
    queryset            = EquipmentCart.objects.all()
    serializer_class    = SlzEquipmentCartInput
    permission_classes  = [ AllowAny ]

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
    serializer_class    = SlzEquipmentCart
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        idCart      = request.data['equipmentCart']
        EquipmentCart.objects.filter(id=idCart, user=account).delete()
        return redirect(reverse('equipmentCartListPage'))

class ConfirmBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        equipments  = EquipmentCart.objects.filter(user=account)
        if not equipments.exists():
            return redirect(reverse('addScientificInstrumentPage'))
        order = Order.objects.create(user=account)
        for item in equipments:
            equipment = Equipment.objects.get(id=item.equipment.id)
            if equipment.quantity < item.quantity:
                return redirect(reverse('addScientificInstrumentPage'))
            equipment.quantity -= item.quantity
            equipment.save()
            borrowing = Borrowing.objects.create(user=account, equipment=item.equipment, quantity=item.quantity)
            order.equipment.add(borrowing)
        equipments.delete()
        return redirect(reverse('notificationsEquipmentPage'))

class DisapprovedBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notificationsEquipmentPage'))
        order       = Order.objects.filter(id=orderID)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.update(status=Order.STATUS.DISAPPROVED)
        return redirect(reverse('notificationsEquipmentPage'))

class ApprovedBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notificationsEquipmentPage'))
        order       = Order.objects.filter(id=orderID)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        for item in order[0].equipment.all():
            equipment:Equipment = Equipment.objects.get(id=item.equipment.id)
            equipment.statistics += 1
            equipment.save()
        order.update(
            status=Order.STATUS.APPROVED,
            approver=account,
            dateApproved=datetime.now(),
            dateReturn=datetime.now() + timedelta(days=7)
        )
        return redirect(reverse('notificationsEquipmentPage'))

class CancelBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        order       = Order.objects.filter(id=orderID, user=account)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.update( status=Order.STATUS.CANCELED)
        return redirect(reverse('borrowingHistoryPage'))

class RemoveBorrowingApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        order       = Order.objects.filter(id=orderID, user=account)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.delete()
        return redirect(reverse('borrowingHistoryPage'))

class ReturningApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        if account.status == Account.STATUS.ADMIN:
            order = Order.objects.filter(id=orderID)
            order.update(status=Order.STATUS.RETURNED, dateReturn=datetime.now())
            return redirect(reverse('notificationsEquipmentPage'))
        order = Order.objects.filter(id=orderID, user=account, status=Order.STATUS.APPROVED)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.update(status=Order.STATUS.RETURNED, dateReturn=datetime.now())
        return redirect(reverse('notificationsEquipmentPage'))
    
class BorrowAgainApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        if account.status == Account.STATUS.ADMIN:
            order = Order.objects.filter(id=orderID)
            order.update(status=Order.STATUS.RETURNED, dateReturn=datetime.now())
            return redirect(reverse('notificationsEquipmentPage'))
        order = Order.objects.filter(id=orderID, user=account, status=Order.STATUS.APPROVED)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        order.update(status=Order.STATUS.WAITING, dateReturn=datetime.now())
        return redirect(reverse('notificationsEquipmentPage'))

class ConfirmreturnApi(LabAPIView):
    queryset            = Order.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        orderID     = self.request.data.get("orderID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notificationsEquipmentPage'))
        order       = Order.objects.filter(id=orderID, status=Order.STATUS.RETURNED)
        if not order.exists():
            return redirect(reverse('notificationsEquipmentPage'))
        for borrowing in order[0].equipment.all():
            borrowing.equipment.quantity += borrowing.quantity
            borrowing.equipment.save()
        order.update(status=Order.STATUS.COMPLETED)
        return redirect(reverse('notificationsEquipmentPage'))