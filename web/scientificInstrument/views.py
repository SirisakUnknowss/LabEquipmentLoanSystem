#Python
import calendar
from datetime import datetime, date, timedelta, time
#Django
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
#Project
from account.models import Account
from base.functions import uploadImage, downloadFile, getDataFile, writeFileExcel, checkTextNone, exportAccountData
from base.permissions import IsAdminAccount
from base.views import LabAPIGetView, LabAPIView, LabListView
from base.variables import STATUS_STYLE
from borrowing.models import Order
from scientificInstrument.admin import BookingModelResource
from scientificInstrument.functions import updateStatusOrder
from scientificInstrument.models import ScientificInstrument, Booking, getClassPath
from scientificInstrument.serializers import SlzScientificInstrumentInput, SlzBookingInput, SlzBooking, SlzBookingOutput, SlzCancelInput, SlzApprovalInput
from settings.base import MEDIA_ROOT

# Create your views here.        

class ListScientificInstrument(LabListView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

class AddScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        try:
            serializerInput = self.get_serializer(data=request.data)
            if not serializerInput.is_valid():
                self.response["error"] = next(iter(serializerInput.errors.values()))[0]
                return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializerInput)
            self.response["result"] = '/scientificInstrument/list'
            return Response(self.response)
        except Exception as ex:
            self.response["error"] = f"{ex}"
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        ScientificInstrument.objects.filter(id=request.POST["dataID"]).delete()
        return redirect(reverse('scientificInstrumentsListPage'))

class EditScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request, *args, **kwargs):
        scientificInstrument = ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"])
        if not scientificInstrument.exists():
            self.response["result"] = '/chemicalSubstance/edit'
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        scientificInstrument.update(
            name        = request.POST["name"],
            number      = request.POST["number"],
            place       = request.POST["place"],
            detail      = request.POST["detail"],
            annotation  = request.POST["annotation"],
            )
        if not(request.FILES.get('upload', False)):
            self.response["result"] = '/scientificInstrument/list'
            return Response(self.response)
        scientificInstrument:ScientificInstrument = scientificInstrument[0]
        upload  = self.request.FILES['upload']
        name    = getClassPath(scientificInstrument, request.POST["name"])
        uploadImage(name, upload, scientificInstrument)
        self.response["result"] = '/scientificInstrument/list'
        return Response(self.response)

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

class ApprovalBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ IsAuthenticated, IsAdminAccount ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzApprovalInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Booking = serializerInput.validated_data['orderID']
        statusStr: str      = serializerInput.validated_data['status']
        updateStatusOrder(self.order, statusStr)
        self.updateApprover()
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

    def updateApprover(self):
        account: Account = self.request.user.account
        self.order.approver = account
        self.order.dateApproved = datetime.now()
        self.order.save(update_fields=["approver", "dateApproved"])

class CancelBookingApi(LabAPIView):
    queryset            = Booking.objects.all()
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzCancelInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Booking = serializerInput.validated_data['orderID']
        self.order.status   = Order.STATUS.CANCELED
        self.order.save(update_fields=["status"])
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

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

class ExportUserBookings(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        fileName = f"UserScientificInstrumentsData"
        queryset = Account.objects.filter(accountBooking__isnull=False).distinct()
        return exportAccountData(queryset, fileName)

class ExportOrderBookings(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        filePath, fileName = self.writeFile()
        return downloadFile(filePath, fileName)

    def writeFile(self):
        userFileDir = "OrderScientificInstrumentsData"
        dirPath = f"{MEDIA_ROOT}/files/{userFileDir}"
        queryset = Booking.objects.all()
        fileName = f"OrderScientificInstrumentsData"
        
        xlsxFile = getDataFile(dirPath, fileName, BookingModelResource, queryset)
        return f"{dirPath}/{xlsxFile}", xlsxFile

class ExportUsesScientificInstruments(LabAPIView):
    permission_classes = [ IsAdminAccount ]

    def get(self, request: Request, *args, **kwargs):
        if bool(request.GET and request.GET['id']):
            id = request.GET['id']
            return self.getWithID(id)
        return self.getAllItems()

    def getWithID(self, id: str):
        queryset = ScientificInstrument.objects.filter(id=id)
        if not queryset.exists(): return
        sc          = queryset[0]
        fileName    = f'Uses_{sc.name}'
        header      = { 'date': 'วันที่จอง', 'start': 'เริ่มใช้', 'end': 'ถึง', 'studentID': 'รหัสนักศึกษา',
                       'name': 'ชื่อ', 'approver': 'ผู้อนุมัติ', 'status': 'สถานะ' }
        orders = Booking.objects.all()
        scList = []
        for order in orders:
            key = order.scientificInstrument.pk
            if key != sc.pk: continue
            approver = None
            if order.approver:
                approver = f'{checkTextNone(order.approver.firstname)} {checkTextNone(order.approver.lastname)}'
            scList.append(
            {
                'date': order.dateBooking,
                'start': order.startBooking,
                'end': order.endBooking,
                'studentID': f'{order.user.studentID}',
                'name': f'{checkTextNone(order.user.firstname)} {checkTextNone(order.user.lastname)}',
                'approver': approver,
                'status': f'{STATUS_STYLE[order.status]["text"]}',
            })
        return writeFileExcel(scList, header, fileName)
            
    def getAllItems(self):
        fileName    = 'Uses_ScientificInstruments'
        header      = { 'number': 'ลำดับ', 'name': 'ชื่ออุปกรณ์วิทยาศาสตร์', 'time': 'จำนวนทั้งหมด' }
        orders      = Booking.objects.all()
        queryset    = ScientificInstrument.objects.filter(statistics__gte=1).order_by('-statistics')
        scs     = []
        number  = 1
        for data in queryset:
            scs.append({
                'number': number,
                'name': data.name,
                'time': data.statistics,
            })
            number += 1
        return writeFileExcel(scs, header, fileName)