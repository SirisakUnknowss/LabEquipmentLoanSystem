#Module
import re
#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Project
from .models import Equipment

class SlzEquipment(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

class SlzEquipmentInput(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = '__all__'

    def validate_name(self, value):
        if value is None:
            raise ValidationError('Please input name equipment.')
        return value