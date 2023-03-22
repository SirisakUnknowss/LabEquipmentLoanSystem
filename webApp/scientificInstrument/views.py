#Python
import calendar
from datetime import datetime, date, timedelta
#Django
from django.core.files.storage import FileSystemStorage
from django.db.models import F
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
#Project
from account.models import Account
from base.views import LabAPIGetView, LabAPIView
from borrowing.models import Order
from scientificInstrument.models import ScientificInstrument, Booking, getClassPath
from scientificInstrument.serializers import SlzScientificInstrumentInput, SlzScientificInstrument, SlzBookingInput, SlzBooking, SlzBookingOutput

# Create your views here.


class AddScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        scientificInstrument    = self.perform_create(serializerInput)
        serializerOutput        = SlzScientificInstrument(scientificInstrument)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('scientific-instruments-list'))
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        scientificInstrument = ScientificInstrument.objects.filter(number=validated.get("number"))
        if scientificInstrument.exists():
            return scientificInstrument.first()
        else:
            scientificInstrument = ScientificInstrument(
                name        = validated.get("name"),
                number      = validated.get("number"),
                place       = validated.get("place"),
                detail      = validated.get("detail"),
                annotation  = validated.get("annotation"),
            )
            scientificInstrument.save()
            if not(self.request.FILES.get('upload', False)):
                return scientificInstrument
            upload      = self.request.FILES['upload']
            fss         = FileSystemStorage()
            name        = getClassPath(scientificInstrument, validated.get("name"))
            file        = fss.save(name, upload)
            file_url    = fss.url(file)
            scientificInstrument.image = file_url
            scientificInstrument.save()
            return scientificInstrument
        
class RemoveScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"]).delete()
        return redirect(reverse('scientific-instruments-list'))

class EditScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        scientificInstrument = ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"])
        if not scientificInstrument.exists():
            return redirect(reverse('scientific-instruments-list'))
        scientificInstrument.update(
            name        =request.POST["name"],
            number      = request.POST["number"],
            place       = request.POST["place"],
            detail      = request.POST["detail"],
            annotation  = request.POST["annotation"],
            )
        if not(request.FILES.get('upload', False)):
            return redirect(reverse('scientific-instruments-list'))
        scientificInstrument:ScientificInstrument = scientificInstrument[0]
        upload      = self.request.FILES['upload']
        fss         = FileSystemStorage()
        name        = getClassPath(scientificInstrument, request.POST["name"])
        file        = fss.save(name, upload)
        file_url    = fss.url(file)
        scientificInstrument.image = file_url
        scientificInstrument.save()
        return redirect(reverse('scientific-instruments-list'))

class GetTimeCanBooking(LabAPIGetView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        try:
            self.id = request.GET['id']
            dateRequest = request.GET['dateRequest']
            self.dateInput = datetime.strptime(dateRequest, '%Y-%m-%d')
            self.response["result"] = self.checkDateTime()
            return Response(self.response)
        except ValueError as ex:
            self.response["error"] = f"{ex}"
            return Response(self.response)
        except Exception as ex:
            errorDateNone = "Please select date for booking."
            self.response["error"] = errorDateNone
            return Response(self.response)
    
    def checkDateTime(self):
        today = date.today()
        tomorrow = datetime.combine((today + timedelta(days=1)), datetime.min.time())
        
        #  and dateInput <= self.lastDateOfMonth()
        if not self.dateInput >= tomorrow and self.dateInput <= self.lastDateOfMonth():
            raise ValueError("date input invalid.")
        if self.isWeekend():
            raise ValueError("Date is Weekend.")
        timeList = list(Booking.Time)
        values_only = []
        for time in timeList:
            try:
                scientificInstrument = ScientificInstrument.objects.get(pk=self.id)
                Booking.objects.get(scientificInstrument=scientificInstrument, dateBooking=self.dateInput, timeBooking=time)
                continue
            except:
                values_only.append(time)
        values_only.remove(Booking.Time._18_00)
        print(values_only)
        return values_only

    def isWeekend(self):
        print(self.dateInput)
        if self.dateInput.weekday() in [5, 6]:
            return True
        return False

    def lastDateOfMonth(self):
        today = date.today() + timedelta(days=31)
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        last_date_of_month = datetime(today.year, today.month, last_day_of_month)
        return last_date_of_month

class BookingScientificInstrumentApi(LabAPIGetView):
    queryset            = Booking.objects.all()
    serializer_class    = SlzBookingInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account                 = request.user.account
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        booking               = self.perform_create(serializerInput, account)
        serializerOutput        = SlzBooking(booking)
        self.response["result"] = serializerOutput.data
        print(self.response)
        return redirect(reverse('scientific-instruments-list'))
    
    def perform_create(self, serializer, account):
        validated = serializer.validated_data
        booking = Booking(
            user = account,
            scientificInstrument = validated.get("scientificInstrument"),
            dateBooking = validated.get("dateBooking"),
            timeBooking = validated.get("timeBooking"),
            )
        booking.save()
        return booking

class DisapprovedBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        bookingID   = self.request.data.get("bookingID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notifications-booking'))
        booking = Booking.objects.filter(id=bookingID)
        if not booking.exists():
            return redirect(reverse('notifications-booking'))
        booking.update(status=Order.STATUS.DISAPPROVED)
        return redirect(reverse('notifications-booking'))

class ApprovedBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        bookingID   = self.request.data.get("bookingID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notifications-booking'))
        booking = Booking.objects.filter(id=bookingID)
        if not booking.exists():
            return redirect(reverse('notifications-booking'))
        booking.update(
            status=Order.STATUS.APPROVED,
            approver=account,
            dateApproved=datetime.now()
        )
        return redirect(reverse('notifications-booking'))

class CancelBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        bookingID   = self.request.data.get("bookingID")
        booking     = Booking.objects.filter(id=bookingID, user=account)
        if not booking.exists():
            return redirect(reverse('information-scientificInstrument'))
        booking.update( status=Order.STATUS.CANCELED)
        return redirect(reverse('notifications-booking'))

class GetBookingByID(LabAPIGetView):
    queryset            = Booking.objects.all()
    serializer_class    = SlzBookingOutput
    permission_classes  = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        id                      = request.GET['id']
        booking                 = get_object_or_404(Booking, pk=id)
        serializer              = self.get_serializer(booking)
        self.response["result"] = serializer.data
        return Response(self.response)