#Django
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
#Project
from chemicalSubstance.models import ChemicalSubstance, HazardCategory

class SlzChemicalSubstance(serializers.ModelSerializer):
    class Meta:
        model = ChemicalSubstance
        fields = '__all__'

    def to_representation(self, instance: ChemicalSubstance):
        response = super(SlzChemicalSubstance, self).to_representation(instance)
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
            raise ValidationError("Error: Invalid name")
        except ChemicalSubstance.DoesNotExist:
            return value

class SlzHazardCategory(serializers.ModelSerializer):
    class Meta:
        model = HazardCategory
        fields = '__all__'