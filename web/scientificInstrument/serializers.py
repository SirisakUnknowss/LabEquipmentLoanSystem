# Python
import os
from datetime import datetime, time
from pythainlp.util import thai_strftime
# Django
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# Project
from account.serializers import SlzAccountCreate
from scientificInstrument.models import ScientificInstrument, Booking, Order

class SlzScientificInstrument(serializers.ModelSerializer):
    class Meta:
        model = ScientificInstrument
        fields = '__all__'

    def to_representation(self, instance):
        response            = super(SlzScientificInstrument, self).to_representation(instance)
        fullPath = os.path.join(settings.MEDIA_URL, f"{instance.image}")
        print(fullPath)
        response["image"]   = fullPath
        return response

class SlzScientificInstrumentInput(serializers.ModelSerializer):
    class Meta:
        model = ScientificInstrument
        fields = '__all__'

    def validate_name(self, value):
        if value is None:
            raise ValidationError('Please input name Scientific Instrument.')
        return value

    def validate_number(self, value):
        if value is None:
            raise ValidationError('Please input numberID Scientific Instrument.')
        return value

class SlzBooking(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class SlzBookingInput(serializers.Serializer):
    scientificInstrument    = serializers.CharField()
    dateBooking             = serializers.CharField()
    startBooking            = serializers.CharField()
    endBooking              = serializers.CharField()

    def validate_scientificInstrument(self, value):
        try:
            self.scientificInstrument = ScientificInstrument.objects.get(pk=value)
            return self.scientificInstrument
        except ScientificInstrument.DoesNotExist:
            raise ValidationError('Not Found ScientificInstrument.')

    def validate_dateBooking(self, value):
        try:
            self.dateBooking = datetime.strptime(value, '%Y-%m-%d').date()
            return self.dateBooking
        except:
            raise ValidationError('date Booking Invalid.')

    def validate_startBooking(self, value):
        try:
            hour = int(value.split(":")[0])
            if 16 > hour >= 8:
                self.startBooking = time(hour, 0)
                return self.startBooking
            raise ValidationError('time start Booking Invalid.')
        except:
            raise ValidationError('time start Booking Invalid.')

    def validate_endBooking(self, value):
        try:
            hour = int(value.split(":")[0])
            if 16 >= hour > 8:
                self.endBooking = time(hour, 0)
                return self.endBooking
            raise ValidationError('time end Booking Invalid.')
        except:
            raise ValidationError('time end Booking Invalid.')

    def validate(self, instance):
        try:
            self.booking = Booking.objects.get(
                scientificInstrument=self.scientificInstrument,
                startBooking=self.startBooking,
                endBooking=self.endBooking,
                dateBooking=self.dateBooking
            )
            raise ValidationError('Booking Exist.')
        except Booking.DoesNotExist:
            instance['amountOfTime'] = self.endBooking.hour - self.startBooking.hour
            return instance

class SlzBookingOutput(serializers.ModelSerializer):
    user                    = SlzAccountCreate(read_only=True)
    scientificInstrument    = SlzScientificInstrument(read_only=True)

    class Meta:
        model   = Booking
        fields  = '__all__'

    def to_representation(self, instance):
        response                = super(SlzBookingOutput, self).to_representation(instance)
        response["dateBooking"] = self.convertToThaiDate(instance.dateBooking)
        response["startBooking"] = f"เวลา {instance.startBooking.strftime('%H:%M')} น."
        response["status"]      = instance.status
        return response

    def convertToThaiDate(self, dateBooking):
        try:
            thai_date_str = thai_strftime(dateBooking, '%e %b %G').replace(' ', '\xa0')
            return thai_date_str
        except:
            return ""

class SlzCancelInput(serializers.Serializer):
    orderID = serializers.CharField()

    def validate_orderID(self, value):
        try:
            order = Booking.objects.get(id=value, status=Order.STATUS.WAITING)
            return order
        except Booking.DoesNotExist:
            raise ValidationError('ไม่พบรายการจองเครื่องมือ')

class SlzApprovalInput(serializers.Serializer):
    orderID = serializers.CharField()
    status  = serializers.CharField()

    def validate_orderID(self, value):
        try:
            order = Booking.objects.get(id=value, status=Order.STATUS.WAITING, approver=None)
            return order
        except Booking.DoesNotExist:
            raise ValidationError('ไม่พบรายการจองเครื่องมือ')

    def validate_status(self, value):
        if not value in [ Order.STATUS.APPROVED, Order.STATUS.DISAPPROVED ]:
            raise ValidationError('สถานะการยืนยันไม่ถูกต้อง')
        return value