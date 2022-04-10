from django.db import models
from django.utils.html import mark_safe

# Create your models here.

def getClassPath(instance, filename):
    className = instance.__class__.__name__
    return "{}/{}".format(className, filename)

class Equipment(models.Model):
    name        = models.CharField(max_length=100, null=True, blank=True)
    quantity    = models.IntegerField(default=0)
    size        = models.IntegerField(null=True, blank=True)
    unit        = models.CharField(max_length=100, null=True, blank=True)
    image       = models.ImageField(upload_to=getClassPath, max_length=100, null=True, blank=True)

    @property
    def thumbnail(self):
        if self.image:
            return mark_safe('<img src="{}" width="250" height="250" />'.format(self.image.url))
        return ""

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']