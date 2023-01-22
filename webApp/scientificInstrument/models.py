#Python
import random
#Django
from django.db import models
from django.utils.html import mark_safe
#Project
from equipment.models import getClassPath
from borrowing.models import Order

# Create your models here.

def getClassPath(instance, filename):
    className = instance.__class__.__name__
    filename  = str(random.randrange(1, 100)) + str(instance.number) + ".png"
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

    @property
    def thumbnail(self):
        if self.image:
            pathImage = str(self.image.url).replace('media/', '')
            return mark_safe('<img src="{}" width="250" height="250" />'.format('/media/' + pathImage))
        return ""

    def __str__(self):
        return self.name

class Booking(models.Model):
    user                    = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountBooking')
    scientificInstrument    = models.ForeignKey(ScientificInstrument, null=True, blank=True, on_delete=models.CASCADE, related_name='scientificInstrumentBooking')
    dateStart               = models.DateTimeField(null=True, blank=True, default=None)
    dateEnd                 = models.DateTimeField(null=True, blank=True, default=None)
    status                  = models.CharField(null=True, blank=True, choices=Order.STATUS.choices, default=Order.STATUS.WAITING, max_length=20)

    def __str__(self):
        return self.scientificInstrument.name + str(self.scientificInstrument.number)