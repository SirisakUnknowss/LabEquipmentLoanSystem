#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Project
from scientificInstrument.models import ScientificInstrument

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