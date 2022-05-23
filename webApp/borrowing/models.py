from django.db import models
#Project
from equipment.models import Equipment

# Create your models here.

class EquipmentCart(models.Model):
    user        = models.OneToOneField(to='account.Account', null=True, blank=True, on_delete=models.SET_NULL, related_name='account')
    equipment   = models.OneToOneField(Equipment, null=True, blank=True, on_delete=models.SET_NULL, related_name='equipment')
    quantity    = models.IntegerField(default=0)
    