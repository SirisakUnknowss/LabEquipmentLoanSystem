# Python
import re
# Django
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.core.validators import MinValueValidator

def getClassPath(instance, filename):
    className = instance.__class__.__name__
    name = instance.name
    name = re.sub(r'[^a-zA-Z]', '', name)
    filename  = str(instance.pk) + str(name) + ".png"
    return "{}/{}".format(className, filename)

class HazardCategory(models.Model):
    
    class CATEGORY(models.TextChoices):
        GHS    = 'ghs', 'GHS'
        UN   = 'un class', 'UN Class'

    serialNumber    = models.CharField(max_length=20, unique=True)
    name            = models.CharField(max_length=100, null=True, blank=True)
    category        = models.CharField(max_length=10, choices=CATEGORY.choices, null=True, blank=True)
    image           = models.ImageField(upload_to=getClassPath, max_length=100, null=True, blank=True)

    @property
    def thumbnail(self):
        if self.image:
            return mark_safe('<img src="{}" width="50" height="50" />'.format(f'/static/images/hazard/{self.serialNumber}.png'))
        return mark_safe('<img src="{}" width="50" height="50" />'.format('/static/images/equipment/PlaceHolder.png'))

    def __str__(self):
        return self.serialNumber

class ChemicalSubstance(models.Model):

    name                = models.CharField(max_length=100)
    serialNumber        = models.CharField(max_length=100)
    casNo               = models.CharField(max_length=100)
    place               = models.CharField(max_length=100)
    initialQuantity     = models.FloatField(default=0, validators=[MinValueValidator(0)])
    remainingQuantity   = models.FloatField(default=0, validators=[MinValueValidator(0)])
    unit                = models.CharField(max_length=100)
    catalogNo           = models.CharField(max_length=100, null=True, blank=True)
    manufacturer        = models.CharField(max_length=100, null=True, blank=True)
    distributor         = models.CharField(max_length=100, null=True, blank=True)
    grade               = models.CharField(max_length=100, null=True, blank=True)
    price               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buyInDate           = models.DateField(null=True, blank=True, default=None)
    activateDate        = models.DateField(null=True, blank=True, default=None)
    expirationDate      = models.DateField(null=True, blank=True, default=None)
    hazardCategory      = models.CharField(max_length=10, null=True, blank=True)
    ghs                 = models.ManyToManyField(HazardCategory, blank=True, related_name='chemicalSubstance_ghs')
    unClass             = models.ManyToManyField(HazardCategory, blank=True, related_name='chemicalSubstance_unClass')
    image               = models.ImageField(upload_to=getClassPath, max_length=100, null=True, blank=True)
    statistics          = models.IntegerField(default=0)

    @property
    def thumbnail(self):
        if self.image:
            pathImage = str(self.image.url).replace('media/', '')
            return mark_safe('<img src="{}" width="250" height="250" />'.format('/media/' + pathImage))
        return mark_safe('<img src="{}" width="50" height="50" />'.format('/static/images/equipment/PlaceHolder.png'))

    def __str__(self):
        return self.name

class Withdrawal(models.Model):
    user                = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountWithdrawal')
    chemicalSubstance   = models.ForeignKey(ChemicalSubstance, null=True, blank=True, on_delete=models.CASCADE, related_name='chemicalSubstanceWithdrawal')
    quantity            = models.IntegerField(default=0)

    def __str__(self):
        return self.chemicalSubstance.name

class Order(models.Model):
    class STATUS(models.TextChoices):
        WAITING     = 'waiting', 'Waiting'
        APPROVED    = 'approved', 'Approved'
        CANCELED    = 'canceled', 'Canceled'
        DISAPPROVED = 'disapproved', 'Disapproved'

    user                = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='userOrderWithdraw')
    chemicalSubstance   = models.ManyToManyField(Withdrawal, default=None)
    dateWithdraw        = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dateApproved        = models.DateTimeField(blank=True, null=True, default=None)
    approver            = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.SET_NULL, related_name='approverWithdraw')
    status              = models.CharField(null=True, blank=True, choices=STATUS.choices, default=STATUS.WAITING, max_length=20)

class ChemicalSubstanceCart(models.Model):
    user                = models.ForeignKey(to='account.Account', null=True, blank=True, on_delete=models.CASCADE, related_name='accountChemicalSubstanceCart')
    chemicalSubstance   = models.ForeignKey(ChemicalSubstance, on_delete=models.CASCADE, related_name='chemicalSubstanceInCart')
    quantity            = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        if self.chemicalSubstance:
            return f"{self.chemicalSubstance.name} ({self.chemicalSubstance.serialNumber})"
        return ""