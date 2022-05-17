
from django import forms
from .models import Equipment


class AddEquipmentForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Equipment
        fields = ('name', 'size', 'quantity', 'unit' ,'image')