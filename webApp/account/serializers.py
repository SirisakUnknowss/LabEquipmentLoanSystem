
# Django
from rest_framework import serializers
#Project
from .models import Account

class SlzAccountCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        exclude = []
        field = '__all__'