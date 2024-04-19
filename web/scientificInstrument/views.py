#Python
import calendar
from datetime import datetime, date, timedelta, time
#Django
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
#Project
from account.models import Account
from base.functions import uploadImage
from base.views import LabAPIGetView, LabAPIView, LabListView
from borrowing.models import Order
from scientificInstrument.models import ScientificInstrument, Booking, getClassPath
from scientificInstrument.serializers import SlzScientificInstrumentInput, SlzScientificInstrument, SlzBookingInput, SlzBooking, SlzBookingOutput

# Create your views here.        

class ListScientificInstrument(LabListView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

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
        return redirect(reverse('scientificInstrumentsListPage'))
    
    def perform_create(self, serializer):
        validated               = serializer.validated_data
        scientificInstrument    = ScientificInstrument.objects.filter(number=validated.get("number"))
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
            upload  = self.request.FILES['upload']
            name    = getClassPath(scientificInstrument, validated.get("name"))
            uploadImage(name, upload, scientificInstrument)
            return scientificInstrument
        
class RemoveScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"]).delete()
        return redirect(reverse('scientificInstrumentsListPage'))

class EditScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        scientificInstrument = ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"])
        if not scientificInstrument.exists():
            return redirect(reverse('scientificInstrumentsListPage'))
        scientificInstrument.update(
            name        = request.POST["name"],
            number      = request.POST["number"],
            place       = request.POST["place"],
            detail      = request.POST["detail"],
            annotation  = request.POST["annotation"],
            )
        if not(request.FILES.get('upload', False)):
            return redirect(reverse('scientificInstrumentsListPage'))
        scientificInstrument:ScientificInstrument = scientificInstrument[0]
        upload  = self.request.FILES['upload']
        name    = getClassPath(scientificInstrument, request.POST["name"])
        uploadImage(name, upload, scientificInstrument)
        return redirect(reverse('scientificInstrumentsListPage'))

class GetTimeStartCanBooking(LabAPIGetView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        try:
            self.id         = request.GET['id']
            dateRequest     = request.GET['dateRequest']
            self.dateInput  = datetime.strptime(dateRequest, '%Y-%m-%d')
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
        if not self.dateInput >= tomorrow and self.dateInput <= self.lastDateOfMonth():
            raise ValueError("date input invalid.")
        # if self.isWeekend():
        #     raise ValueError("Date is Weekend.")
        times = list()
        
        scientificInstrument = ScientificInstrument.objects.get(pk=self.id)
        bookings = Booking.objects.filter(scientificInstrument=scientificInstrument, dateBooking=self.dateInput)
        listTimeDefault = [8, 9, 10, 11, 12, 13, 14, 15]
        listTimeUse = []
        for booking in bookings:
            for x in range(booking.startBooking.hour, booking.endBooking.hour):
                listTimeUse.append(x)
        listTime = [x for x in listTimeDefault if x not in listTimeUse]

        for x in listTime:
            times.append(time(x, 0))
        return times

    def isWeekend(self):
        if self.dateInput.weekday() in [5, 6]:
            return True
        return False

    def lastDateOfMonth(self):
        today               = date.today() + timedelta(days=31)
        last_day_of_month   = calendar.monthrange(today.year, today.month)[1]
        last_date_of_month  = datetime(today.year, today.month, last_day_of_month)
        return last_date_of_month

class GetTimeEndCanBooking(LabAPIGetView):
    permission_classes = [ AllowAny ]

    def get(self, request, *args, **kwargs):
        try:
            self.id         = request.GET['id']
            dateRequest     = request.GET['dateRequest']
            timeStart       = request.GET['timeStart']
            self.dateInput  = datetime.strptime(dateRequest, '%Y-%m-%d')
            times = list()
            
            scientificInstrument = ScientificInstrument.objects.get(pk=self.id)
            bookings = Booking.objects.filter(scientificInstrument=scientificInstrument, dateBooking=self.dateInput)
            listTimeDefault = [9, 10, 11, 12, 13, 14, 15, 16]
            listTimeUse = []
            for booking in bookings:
                for x in range(booking.startBooking.hour + 1, booking.endBooking.hour + 1):
                    listTimeUse.append(x)
            listTime = [x for x in listTimeDefault if x not in listTimeUse]
            
            if timeStart != "":
                hour = int(timeStart.split(":")[0])
                lastTime = 0
                for x in listTime:
                    if lastTime != 0 and x != lastTime + 1:
                        break
                    if x < hour + 1: 
                        continue
                    times.append(time(x, 0))
                    lastTime = x
            self.response["result"] = times
            return Response(self.response)
        except ValueError as ex:
            self.response["error"] = f"{ex}"
            return Response(self.response)
        except Exception as ex:
            errorDateNone = "Please select time for booking."
            self.response["error"] = errorDateNone
            return Response(self.response)

class BookingScientificInstrumentApi(LabAPIGetView):
    queryset            = Booking.objects.all()
    serializer_class    = SlzBookingInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account                 = request.user.account
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        booking                 = self.perform_create(serializerInput, account)
        serializerOutput        = SlzBooking(booking)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('scientificInstrumentsListPage'))
    
    def perform_create(self, serializer, account):
        validated = serializer.validated_data
        booking = Booking(
            user = account,
            scientificInstrument = validated.get("scientificInstrument"),
            dateBooking = validated.get("dateBooking"),
            startBooking = validated.get("startBooking"),
            endBooking = validated.get("endBooking"),
            amountOfTime = validated.get("amountOfTime")
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
            return redirect(reverse('notificationBookingPage'))
        booking = Booking.objects.filter(id=bookingID)
        if not booking.exists():
            return redirect(reverse('notificationBookingPage'))
        booking.update(status=Order.STATUS.DISAPPROVED)
        return redirect(reverse('notificationBookingPage'))

class ApprovedBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        bookingID   = self.request.data.get("bookingID")
        if account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notificationBookingPage'))
        booking = Booking.objects.filter(id=bookingID)
        if not booking.exists():
            return redirect(reverse('notificationBookingPage'))
        booking.update(
            status=Order.STATUS.APPROVED,
            approver=account,
            dateApproved=datetime.now()
        )
        scientificInstrument = booking.first().scientificInstrument
        scientificInstrument.statistics += 1
        scientificInstrument.save(update_fields=['statistics'])
        
        return redirect(reverse('notificationBookingPage'))

class CancelBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        bookingID   = self.request.data.get("bookingID")
        booking     = Booking.objects.filter(id=bookingID, user=account)
        if not booking.exists():
            return redirect(reverse('notificationBookingPage'))
        booking.update( status=Order.STATUS.CANCELED)
        return redirect(reverse('notificationBookingPage'))

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