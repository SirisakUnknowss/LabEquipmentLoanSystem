# Python
import json
# Django
from django.db.models import Q, Count
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.request import Request
# Project
from account.models import Account
from base.menu import MenuList, AdminOnly
from base.variables import STATUS_STYLE
from scientificInstrument.models import ScientificInstrument, Booking, Order
from scientificInstrument.serializers import SlzScientificInstrument

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
            bookingsAll             = Booking.objects.filter(scientificInstrument=scientificInstrument).order_by('-dateBooking', '-startBooking')
        except:
            bookingsAll = Booking.objects.all().order_by('-dateBooking', '-startBooking')
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

class ListPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, 1)
        results                     = ScientificInstrument.objects.all().order_by('name')
        serializer                  = SlzScientificInstrument(results, many=True).data
        resultsJson                 = json.dumps(serializer, ensure_ascii=False)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = '/api/scientificInstrument/remove'
        return render(request, 'pages/scientificInstruments/listPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(1, 1)
        nameSearch                  = request.POST['nameSearch']
        name                        = Q(name__contains=nameSearch)
        results                     = ScientificInstrument.objects.filter(name).order_by('name')
        resultsJson                 = serializers.serialize("json", results)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = '/api/scientificInstrument/remove'
        return render(request, 'pages/scientificInstruments/listPage.html', self.context)

class AddPageView(AdminOnly):

    def get(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).get(request)
        self.context['titleBar']    = 'เพิ่มเครื่องมือวิทยาศาตร์'
        self.context['confirmUrl']  = '/api/scientificInstrument/add'
        return render(request, 'pages/scientificInstruments/addPage.html', self.context)

class EditPageView(AdminOnly):

    def post(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).post(request)
        try:
            result                      = ScientificInstrument.objects.get(id=request.POST['id'])
            self.context['result']      = result
            self.context['titleBar']    = 'แก้ไขเครื่องมือวิทยาศาตร์'
            self.context['confirmUrl']  = '/api/scientificInstrument/edit'
            return render(request, 'pages/scientificInstruments/addPage.html', self.context)
        except ScientificInstrument.DoesNotExist:
            return redirect(reverse('scientificInstrumentsListPage'))

class DetailBookingView(MenuList):

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(1, None)
        try:
            order                       = Booking.objects.get(id=request.POST['id'])
            self.context['order']       = order
            self.context['statusMap']   = STATUS_STYLE
            return render(request, 'pages/scientificInstruments/detailPage.html', self.context)
        except Booking.DoesNotExist:
            return redirect(reverse('notificationBookingPage'))

        
def getOrder(status: int, account: Account, context: dict):
    waiting     = Q(status=Order.STATUS.WAITING)
    if status == 0:
        orders = Booking.objects.filter(waiting)
    if status == 1:
        orders = Booking.objects.exclude(waiting)
    if account.status == Account.STATUS.USER:
        orders = orders.filter(user=account)
    context['orders']      = orders.order_by('-dateBooking', '-startBooking')
    context['statusMap']   = STATUS_STYLE
    return context

class NotificationsBookingView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, -1)
        self.context = getOrder(0, request.user.account, self.context)
        return render(request, 'pages/scientificInstruments/notificationPage.html', self.context)

class BookingHistoryView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(1, 4)
        self.context = getOrder(1, request.user.account, self.context)
        return render(request, 'pages/scientificInstruments/historyPage.html', self.context)

class AnalysisView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notFoundPage'))
        self.addMenuPage(1, 5)
        self.getHistory()
        self.context['orders']      = self.orderAll()
        self.context['accounts']    = self.getAccountNumber()
        self.context['items']       = self.getItemData()
        return render(request, 'pages/scientificInstruments/analysisPage.html', self.context)

    def getItemData(self):
        items       = ScientificInstrument.objects.filter(statistics__gte=1).order_by('-statistics')
        orderDict   = { 'list': items , 'count': items.count() }
        return orderDict

    def getAccountNumber(self) -> int:
        return Account.objects.filter(accountBooking__isnull=False).distinct().count()

    def orderAll(self):
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
        return order

    def getHistory(self):
        self.context['histories']   = {}
        self.context['histories']   = getOrder(1, self.request.user.account, self.context['histories'])
        self.context['histories']['count'] = self.context['histories']['orders'].count()