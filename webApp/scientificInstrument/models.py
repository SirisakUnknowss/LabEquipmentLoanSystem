#Python
import re
from django.utils import timezone

#Django
from django.db import models
from django.utils.html import mark_safe
#Project
from equipment.models import getClassPath
from borrowing.models import Order

# Create your models here.

def getClassPath(instance, filename):
    className = instance.__class__.__name__
    name = instance.name
    name = re.sub(r'[^a-zA-Z]', '', name)
    filename  = str(instance.pk) + str(name) + ".png"
    return "{}/{}".format(className, filename)

class ScientificInstrument(models.Model):
        
    """
    Inherited fields:
    password, last_login, is_active
    """
    name        = models.CharField(max_length=100, null=True, blank=True)
    place       = models.CharField(max_length=100, null=True, blank=True)
    number      = models.CharField(max_length=100, unique=True)
    detail      = models.TextField(null=True, blank=True, default=None)
    annotation  = models.TextField(null=True, blank=True, default=None)
    image       = models.ImageField(upload_to=getClassPath, max_length=100, null=True, blank=True)
    statistics  = models.IntegerField(default=0)

    @property
    def thumbnail(self):
        if self.image:
            pathImage = str(self.image.url).replace('media/', '')
            return mark_safe('<img src="{}" width="250" height="250" />'.format('/media/' + pathImage))
        return ""

    def __str__(self):
        return self.name

class Booking(models.Model):
    class Time(models.TextChoices):
        _9_00     = '09:00 - 10:00'
        _10_00    = '10:00 - 11:00'
        _11_00    = '11:00 - 12:00'
        _12_00    = '12:00 - 13:00'
        _13_00    = '13:00 - 14:00'
        _14_00    = '14:00 - 15:00'
        _15_00    = '15:00 - 16:00'
        _16_00    = '16:00 - 17:00'
        _17_00    = '17:00 - 18:00'
        _18_00    = '18:00 - 19:00'
    
    user                    = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountBooking')
    scientificInstrument    = models.ForeignKey(ScientificInstrument, null=True, blank=True, on_delete=models.CASCADE, related_name='scientificInstrumentBooking')
    dateBooking             = models.DateField(null=True, blank=True, default=None)
    timeBooking             = models.CharField(max_length=20, choices=Time.choices, null=True, blank=True)
    startBooking            = models.TimeField(blank=True, null=True, default=None)
    endBooking              = models.TimeField(blank=True, null=True, default=None)
    amountOfTime            = models.IntegerField(default=1)
    dateApproved            = models.DateTimeField(blank=True, null=True, default=None)
    approver                = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.SET_NULL, related_name='accountApproverBooking')
    status                  = models.CharField(null=True, blank=True, choices=Order.STATUS.choices, default=Order.STATUS.WAITING, max_length=20)
    createAt                = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.scientificInstrument:
            return str(self.scientificInstrument.name) + str(self.scientificInstrument.number) + str(self.dateBooking) + str(self.timeBooking)
        return ""