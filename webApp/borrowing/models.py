from django.db import models
from django.utils import timezone
from datetime import date, datetime, timedelta
#Project
from equipment.models import Equipment

# Create your models here.

class EquipmentCart(models.Model):
    user        = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountEquipmentCart')
    equipment   = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.CASCADE, related_name='equipmentEquipmentCart')
    quantity    = models.IntegerField(default=0)

    def __str__(self):
        return self.equipment.name + str(self.equipment.size)

class Borrowing(models.Model):
    user        = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountBorrowing')
    equipment   = models.ForeignKey(Equipment, null=True, blank=True, on_delete=models.CASCADE, related_name='equipmentBorrowing')
    quantity    = models.IntegerField(default=0)

    def __str__(self):
        return self.equipment.name + str(self.equipment.size)

class Order(models.Model):
    class STATUS(models.TextChoices):
        WAITING     = 'waiting', 'Waiting'
        APPROVED    = 'approved', 'Approved'
        CANCELED   = 'canceled', 'Canceled'
        DISAPPROVED = 'disapproved', 'Disapproved'
        COMPLETED   = 'completed', 'Completed'
        OVERDUED    = 'overdued', 'Overdued'
        RETURNED    = 'returned', 'Returned'
    user            = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountOrder')
    equipment       = models.ManyToManyField(Borrowing, default=None)
    dateBorrowing   = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dateApproved    = models.DateTimeField(blank=True, null=True, default=None)
    dateReturn      = models.DateTimeField(blank=True, null=True, default=None)
    approver        = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.SET_NULL, related_name='account')
    status          = models.CharField(null=True, blank=True, choices=STATUS.choices, default=STATUS.WAITING, max_length=20)
            
    @property
    def quantity(self):
        return self.equipment.count()