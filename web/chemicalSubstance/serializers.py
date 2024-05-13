#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Project
from chemicalSubstance.models import ChemicalSubstance, HazardCategory, Order

class SlzChemicalSubstanceOutput(serializers.ModelSerializer):
    class Meta:
        model = ChemicalSubstance
        fields = '__all__'

    def to_representation(self, instance: ChemicalSubstance):
        response = super(SlzChemicalSubstanceOutput, self).to_representation(instance)
        response['catalogNo']       = self.checkNone(instance.catalogNo)
        response['distributor']     = self.checkNone(instance.distributor)
        response['manufacturer']    = self.checkNone(instance.manufacturer)
        response['grade']           = self.checkNone(instance.grade)
        response['buyInDate']       = self.checkNone(instance.buyInDate)
        response['activateDate']    = self.checkNone(instance.activateDate)
        response['expirationDate']  = self.checkNone(instance.expirationDate)
        response['ghs']             = instance.ghs.values_list('serialNumber', flat=True)
        response['unClass']         = instance.unClass.values_list('serialNumber', flat=True)
        return response

    def checkNone(self, data):
        if str(data) == "None":
            return ""
        return data

class SlzChemicalSubstanceInput(serializers.ModelSerializer):
    ghs     = serializers.SlugRelatedField(many=True, read_only=True, slug_field='ghs')
    unClass = serializers.SlugRelatedField(many=True, read_only=True, slug_field='unClass')
    class Meta:
        model = ChemicalSubstance
        fields = '__all__'

    def validate_name(self, value):
        try:
            instance = ChemicalSubstance.objects.get(name=value)
            raise ValidationError("ชื่อสารเคมีไม่ถูกต้อง")
        except ChemicalSubstance.DoesNotExist:
            return value

    def validate(self, instance):
        print(instance['expirationDate'])
        initialQuantity     = float(instance['initialQuantity'])
        remainingQuantity   = float(instance['remainingQuantity'])
        if remainingQuantity > initialQuantity:
            raise ValidationError("ปริมาณคงเหลือไม่ถูกต้อง")
        return instance

class SlzHazardCategory(serializers.ModelSerializer):
    class Meta:
        model = HazardCategory
        fields = '__all__'

class SlzApprovalInput(serializers.Serializer):
    orderID = serializers.CharField()
    status  = serializers.CharField()

    def validate_orderID(self, value):
        try:
            order = Order.objects.get(id=value, status=Order.STATUS.WAITING, approver=None)
            return order
        except Order.DoesNotExist:
            raise ValidationError('ไม่พบรายการเบิกสารเคมี')

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
            raise ValidationError('ไม่พบรายการเบิกสารเคมี')

class SlzConfirmWithdrawalInput(serializers.Serializer):
    orderList = serializers.ListField(child=serializers.JSONField())

    def validate_orderList(self, value):
        self.orderValidate = []
        for order in value:
            if type(order) is not dict: continue
            if not ('id' in order and 'quantity' in order): continue
            self.idChemical = order['id']
            self.quantity   = float(order['quantity'])
            try:
                order['chemicalSubstance'] = SlzChemicalSubstanceOutput(ChemicalSubstance.objects.get(id=self.idChemical)).data
                if order['chemicalSubstance']['remainingQuantity'] < self.quantity:
                    raise ValidationError('ปริมาณสารเคมีที่เบิกมีไม่เพียงพอ')
                self.orderValidate.append({ 'chemicalSubstance': order['chemicalSubstance'], 'quantity': self.quantity })
            except ChemicalSubstance.DoesNotExist:
                raise ValidationError('ไม่พบสารเคมี')
        return self.orderValidate

class SlzOrderOutput(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'