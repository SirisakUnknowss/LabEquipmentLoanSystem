# Django
from django.core import serializers
from rest_framework.request import Request
# Project
from base.views import *


class CalendarView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, 2)
        self.scientificInstruments()
        self.context['scientificInstrumentID'] = None
        self.bookings()
        return render(request, 'pages/scientificInstruments/calendarPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, 2)
        self.context['scientificInstrumentID'] = request.POST["scientificInstrumentID"]
        self.scientificInstruments()
        self.bookings()
        return render(request, 'pages/scientificInstruments/calendarPage.html', self.context)

    def scientificInstruments(self):
        scientificInstrumentsAll        = ScientificInstrument.objects.all()
        scientificInstrument            = dict()
        scientificInstrument['all']     = scientificInstrumentsAll.count()
        scientificInstrument['data']    = scientificInstrumentsAll
        self.context['scientificInstruments'] = scientificInstrument

    def bookings(self):
        try:
            id = self.context['scientificInstrumentID']
            scientificInstrument    = ScientificInstrument.objects.get(pk=int(id))
            bookingsAll             = Booking.objects.filter(scientificInstrument=scientificInstrument).order_by('-dateBooking', '-timeBooking')
        except:
            bookingsAll = Booking.objects.all().order_by('-dateBooking', '-timeBooking')
        booking         = dict()
        booking['all']  = bookingsAll.count()
        booking['data'] = self.getBookingList(bookingsAll)
        self.context['bookings'] = booking

    def getBookingList(self, bookingsAll):
        bookingList = []
        for booking in bookingsAll:
            booking: Booking = booking
            day ="{:02d}".format(booking.dateBooking.day)
            month = "{:02d}".format(booking.dateBooking.month)
            year = booking.dateBooking.year
            jsonData = {}
            jsonData["title"] = f"{booking.scientificInstrument.name}"
            jsonData["start"] = f"{year}-{month}-{day}"
            jsonData["url"] = booking.pk
            bookingList.append(jsonData)
        return (str(bookingList)).replace("\'", "\"")

class SIListPageView(MenuList):
    def process_request(self, request):
        self.addMenuPage(1, 1)
        scientificInstruments = ScientificInstrument.objects.all().order_by('number')

        if request.method == 'POST':
            nameScientificInstrument = request.POST.get('nameScientificInstrument', '')
            name = Q(name__contains=nameScientificInstrument)
            number = Q(number__contains=nameScientificInstrument)
            scientificInstruments = ScientificInstrument.objects.filter(name | number).order_by('name')

        scientificInstrumentsJson = serializers.serialize("json", scientificInstruments)
        self.context['scientificInstruments'] = scientificInstruments
        self.context['scientificInstrumentsJson'] = scientificInstrumentsJson

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.process_request(request)
        return render(request, 'pages/scientificInstruments/listPage.html', self.context)

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.process_request(request)
        return render(request, 'pages/scientificInstruments/listPage.html', self.context)

class AddPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        return render(request, 'pages/scientificInstruments/add_scientific_instruments.html')

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        if request.method == 'POST':
            scientificInstrumentID = request.POST['ScientificInstrumentID']
            scientificInstrument = ScientificInstrument.objects.filter(id=scientificInstrumentID)
            if scientificInstrument.exists():
                self.context['scientificInstrument'] = scientificInstrument.first()
                return render(request, 'pages/scientificInstruments/add_scientific_instruments.html', self.context)
            return redirect(reverse('scientificInstrumentsListPage'))

# def informationBookingPage(request):
#     if not(request.user.is_authenticated): return redirect(reverse('homepage'))
#     waiting     = Q(status=Order.STATUS.WAITING)
#     approved    = Q(status=Order.STATUS.APPROVED)
#     bookings    = Booking.objects.filter(waiting | approved)
#     if request.user.account.status == Account.STATUS.USER:
#         bookings  = bookings.filter(user=request.user.account)
#     context     = { 'bookings': bookings.order_by('-dateBooking', '-timeBooking') }
#     return render(request, 'pages/scientificInstruments/informationPage.html', context)


class DetailBookingView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, -1)
        return redirect(reverse('notificationBookingPage'))

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(1, -1)
        bookingID = request.POST.get('bookingID')
        booking = Booking.objects.filter(id=bookingID).first()
        if booking is not None:
            self.context['booking'] = booking
            return render(request, 'pages/scientificInstruments/detail_page.html', self.context)
        return redirect(reverse('notificationBookingPage'))

class NotificationsBookingView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, -1)
        account     = request.user.account
        bookings    = self.getBookings(account)
        self.context['bookings'] = bookings.order_by('-dateBooking', '-timeBooking')
        return render(request, 'pages/scientificInstruments/notificationPage.html', self.context)

    def getBookings(self, account: Account):
        waiting     = Q(status=Order.STATUS.WAITING)
        approved    = Q(status=Order.STATUS.APPROVED)
        bookings = Booking.objects.filter(user=account).filter(approved | waiting)
        if account.status == Account.STATUS.ADMIN:
            waiting     = Q(status=Order.STATUS.WAITING)
            bookings      = Booking.objects.filter(waiting)
        return bookings

class AnalysisPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, 3)
        self.topScientificInstrument()
        self.bookingAll()
        return render(request, 'pages/scientificInstruments/analysisPage.html', self.context)

    def topScientificInstrument(self):
        scientificInstruments = ScientificInstrument.objects.all().order_by('-statistics').filter(statistics__gt=1)[:20]
        self.context['scientificInstruments'] = scientificInstruments

    def bookingAll(self):
        waiting     = Q(status=Order.STATUS.WAITING)
        approved    = Q(status=Order.STATUS.APPROVED)
        canceled    = Q(status=Order.STATUS.CANCELED)
        disapproved = Q(status=Order.STATUS.DISAPPROVED)
        order       = dict()
        bookings    = Booking.objects.all()

        order['all']            = bookings.count()
        order['waiting']        = bookings.filter(waiting).count()
        order['canceled']       = bookings.filter(canceled).count()
        order['approved']       = bookings.filter(approved).count()
        order['disapproved']    = bookings.filter(disapproved).count()
        self.context['bookings'] = order