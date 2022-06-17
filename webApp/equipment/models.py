import random
from django.db import models
from django.utils.html import mark_safe

# Create your models here.

def getClassPath(instance, filename):
    className = instance.__class__.__name__
    filename  = str(random.randrange(1, 100)) + instance.unit + str(instance.size) + str(instance.unit) + ".png"
    return "{}/{}".format(className, filename)

class Equipment(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    quantity    = models.IntegerField(default=0)
    size        = models.IntegerField(null=True, blank=True)
    unit        = models.CharField(max_length=100, null=True, blank=True)
    brand       = models.CharField(max_length=100, null=True, blank=True)
    image       = models.ImageField(upload_to=getClassPath, max_length=100, null=True, blank=True)

    @property
    def thumbnail(self):
        if self.image:
            pathImage = str(self.image.url).replace('media/', '')
            return mark_safe('<img src="{}" width="250" height="250" />'.format('/media/' + pathImage))
        return ""

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']