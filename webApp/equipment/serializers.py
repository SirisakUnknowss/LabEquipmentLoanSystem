#Django
from rest_framework import serializers
#Project
from .models import Equipment

class SlzEquipment(serializers.ModelSerializer):
    class Meta:
        model = Equipment

class SlzEquipmentInput(SlzEquipment):
    class Meta:
        model = Equipment
        exclude  = [ 'id' ]

    # def validate_name(self, value):