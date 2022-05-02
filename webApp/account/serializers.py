
# Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Project
from .models import Account

class SlzAccountCreate(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        exclude = []
        field = '__all__'

# class SlzAuthenOTP(serializers.Serializer):
    # studentID = serializers.CharField(max_length=10)
    # password    = serializers.CharField(max_length=100, default='12345678')
    # email       = serializers.EmailField(null=True, blank=True)
    # firstname   = serializers.CharField(max_length=100)
    # lastname    = serializers.CharField(max_length=100)
    # gender      = serializers.CharField(max_length=50)
    # phone       = serializers.CharField(max_length=10)
    # levelclass  = serializers.CharField(max_length=2)
    # branch      = serializers.CharField(max_length=100)
    # faculty     = serializers.CharField(max_length=100)
    # status      = serializers.CharField(max_length=10)


    # def validate_idToken(self, value):
    #     try:
    #         res = auth.verify_id_token(value)
    #         mobile = res['phone_number']
    #         uid = res['uid']
    #     except Exception as error:
    #         raise ValidationError(error)
    #     return mobile, uid 