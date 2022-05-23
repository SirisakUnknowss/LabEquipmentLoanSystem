#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

#Project
from .models import EquipmentCart
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
        equipment = instance['equipment']
        quantity = instance['quantity']
        if quantity > equipment.quantity :
            raise ValidationError('Not Enough Equipment.')
        return instance