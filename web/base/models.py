from django.db import models

# Create your models here.
class DataWeb(models.Model):
    linkAssessmentForm  = models.CharField(null=True, blank=True, max_length=1000)
    fileUserManual      = models.FileField(upload_to='file/', null=True, blank=True)