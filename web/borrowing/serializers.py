#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

#Project
from account.models import Account
from borrowing.models import EquipmentCart, Order
from equipment.models import Equipment

class SlzEquipmentCart(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCart
        fields = '__all__'

class SlzEquipmentCartInput(serializers.ModelSerializer):
    class Meta:
        model = EquipmentCart
        fields = '__all__'

    def validate_equipment(self, value):
        equipment = Equipment.objects.filter(pk=value.id)
        if not equipment.exists():
            raise ValidationError('Not Found Equipment.')
        return equipment[0]

    def validate(self, instance):
        equipment   = instance['equipment']
        quantity    = instance['quantity']
        if quantity <= 0:
            raise ValidationError('quantity invalid.')
        if quantity > equipment.quantity:
            raise ValidationError('Not Enough Equipment.')
        return instance


class SlzApprovalInput(serializers.Serializer):
    orderID = serializers.CharField()
    status  = serializers.CharField()

    def validate_orderID(self, value):
        try:
            order = Order.objects.get(id=value, status=Order.STATUS.WAITING, approver=None)
            return order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')

    def validate_status(self, value):
        if not value in [ Order.STATUS.APPROVED, Order.STATUS.DISAPPROVED ]:
            raise ValidationError('สถานะการยืนยันไม่ถูกต้อง')
        return value

class SlzCancelInput(serializers.Serializer):
    orderID = serializers.CharField()

    def validate_orderID(self, value):
        try:
            order = Order.objects.get(id=value, status=Order.STATUS.WAITING)
            return order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')

class SlzReturnInput(serializers.Serializer):
    account = serializers.CharField()
    orderID = serializers.CharField()

    def validate_account(self, value):
        try:
            self.account = Account.objects.get(id=value)
            return self.account
        except Account.DoesNotExist:
            raise ValidationError('ไม่พบบัญชีผู้ใช้งาน')

    def validate_orderID(self, value):
        try:
            self.order = Order.objects.get(id=value)
            return self.order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')

    def validate(self, instance):
        account: Account = instance['account']
        order: Order     = instance['orderID']
        if (account.status == Account.STATUS.ADMIN and order.status == Order.STATUS.OVERDUED) or (order.user == account and order.status == Order.STATUS.APPROVED):
            return instance
        else:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')

class SlzConfirmReturnInput(serializers.Serializer):
    orderID = serializers.CharField()

    def validate_orderID(self, value):
        try:
            self.order = Order.objects.get(id=value, status = Order.STATUS.RETURNED)
            return self.order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')

class SlzBorrowingAgainInput(serializers.Serializer):
    orderID = serializers.CharField()

    def validate_orderID(self, value):
        try:
            self.order = Order.objects.get(id=value, status = Order.STATUS.APPROVED)
            return self.order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการยืม - คืนอุปกรณ์')