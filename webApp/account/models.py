from django.db import models
from django.core.validators import MinValueValidator


LEVEL_CLASS = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10')
]

STATUS_ACCOUNT = [
    ('user', 'user'),
    ('admin', 'admin'),
]

class Account(models.Model):
    """
    Inherited fields:
    password, last_login, is_active
    """
    studentID   = models.CharField(max_length=100, unique=True)
    password    = models.CharField(max_length=100, validators=[MinValueValidator(8)], default='12345678')
    email       = models.EmailField(null=True, blank=True)
    firstname   = models.CharField(max_length=100, null=True, blank=True)
    lastname    = models.CharField(max_length=100, null=True, blank=True)
    gender      = models.CharField(max_length=50, null=True, blank=True)
    phone       = models.CharField(max_length=10, null=True, blank=True)
    levelclass  = models.CharField(max_length=2, choices=LEVEL_CLASS, null=True, blank=True)
    branch      = models.CharField(max_length=100, null=True, blank=True)
    faculty     = models.CharField(max_length=100, null=True, blank=True)
    status      = models.CharField(max_length=10, choices=STATUS_ACCOUNT, null=True, blank=True)

