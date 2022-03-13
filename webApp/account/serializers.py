
# Django
from rest_framework import serializers
from .models import Account

class SlzAccountCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Account