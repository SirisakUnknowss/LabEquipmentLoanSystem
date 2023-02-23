# Python
from datetime import datetime
# Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
# Project
from scientificInstrument.models import ScientificInstrument, Booking

class SlzScientificInstrument(serializers.ModelSerializer):
    class Meta:
        model = ScientificInstrument
        fields = '__all__'

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
    timeBooking             = serializers.CharField()

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

    def validate_timeBooking(self, value):
        if value in Booking.Time:
            self.timeBooking = value
            return self.timeBooking
        raise ValidationError('time Booking Invalid.')

    def validate(self, instance):
        try:
            self.booking = Booking.objects.get(
                scientificInstrument=self.scientificInstrument,
                timeBooking=self.timeBooking,
                dateBooking=self.dateBooking
            )
            raise ValidationError('Booking Exist.')
        except Booking.DoesNotExist:
            return instance