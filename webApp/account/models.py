from django.db import models
from django.contrib.auth.models import User

from borrowing.models import EquipmentCart, Order
from scientificInstrument.models import Booking
# Module
from django.db.models import Q

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

class Account(models.Model):
    
    class STATUS(models.TextChoices):
        USER    = 'user', 'user'
        ADMIN   = 'admin', 'admin'
    
    class LEVEL_CLASS(models.TextChoices):
        ZERO    = 0, '0'
        ONE     = 1, '1'
        TWO     = 2, '2'
        THREE   = 3, '3'
        FOUR    = 4, '4'
        FIVE    = 5, '5'
        SIX     = 6, '6'
        SEVEN   = 7, '7'
        EIGHT   = 8, '8'
        NINE    = 9, '9'
        TEN     = 10, '10'

    class CATEGORY(models.TextChoices):
        STUDENT         = 'student', 'student'
        TEACHER         = 'teacher', 'teacher'
        PERSONNEL       = 'personnel', 'personnel'
        OTHER           = 'other', 'other'
        USER            = 'user', 'user'
        NOTSPECIFIED    = 'notSpecified', 'notSpecified'
        
    """
    Inherited fields:
    password, last_login, is_active
    """
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    studentID   = models.CharField(max_length=100, unique=True)
    password    = models.CharField(max_length=100, default='12345678')
    email       = models.EmailField(null=True, blank=True)
    nameprefix  = models.CharField(max_length=50, null=True, blank=True)
    firstname   = models.CharField(max_length=100, null=True, blank=True)
    lastname    = models.CharField(max_length=100, null=True, blank=True)
    phone       = models.CharField(max_length=10, null=True, blank=True)
    levelclass  = models.CharField(max_length=2, choices=LEVEL_CLASS.choices, null=True, blank=True)
    branch      = models.CharField(max_length=100, null=True, blank=True)
    faculty     = models.CharField(max_length=100, null=True, blank=True)
    category    = models.CharField(max_length=20, choices=CATEGORY.choices, null=True, blank=True)
    categoryOther = models.CharField(max_length=100, null=True, blank=True)
    status      = models.CharField(max_length=10, choices=STATUS.choices, null=True, blank=True)

    def __str__(self):
        return self.studentID

    @property
    def equipmentcartcount(self):
        count = EquipmentCart.objects.filter(user__studentID=self.studentID).count()
        if count > 9:
            count = "9+"
        return count

    @property
    def orderoverduedcount(self):
        count = Order.objects.filter(user__studentID=self.studentID, status=Order.STATUS.OVERDUED).count()
        if count > 9:
            count = "9+"
        return count

    @property
    def bookingoverduedcount(self):
        waiting     = Q(status=Order.STATUS.WAITING)
        approved    = Q(status=Order.STATUS.APPROVED)
        count = Booking.objects.filter(user__studentID=self.studentID).filter(waiting | approved).count()
        if count > 9:
            count = "9+"
        return count

    @property
    def orderwaitingcount(self):
        if self.status == Account.STATUS.ADMIN:
            returned    = Q(status=Order.STATUS.RETURNED)
            waiting     = Q(status=Order.STATUS.WAITING)
            overdued    = Q(status=Order.STATUS.OVERDUED)
            count       = Order.objects.filter(returned | waiting | overdued).count()
            if count > 9:
                count = "9+"
            return count
        return 0

    @property
    def bookingwaitingcount(self):
        if self.status == Account.STATUS.ADMIN:
            waiting = Q(status=Order.STATUS.WAITING)
            count   = Booking.objects.filter(waiting).count()
            if count > 9:
                count = "9+"
            return count
        return 0