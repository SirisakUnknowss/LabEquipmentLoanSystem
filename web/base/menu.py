# Python
import datetime as DT
# Django
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
# Project
from account.models import Account
from borrowing.models import Order
from chemicalSubstance.functions import cancelOrder
from chemicalSubstance.models import Order as CSOrder

def getOrder(order, status, account: Account):
    orders = order.objects.filter(user=account, status=status)
    if account.status == Account.STATUS.ADMIN:
        orders = order.objects.filter(status=status)
    return orders

def checkOverdue(request: WSGIRequest):
    account: Account = request.user.account
    orders = getOrder(Order, Order.STATUS.APPROVED, account)
    if orders == None: orders
    try:
        orders = orders.filter(dateReturn__lt=timezone.now()).update(status=Order.STATUS.OVERDUED)
    except Exception as ex:
        print(ex)
        print("----------------------------------------")

# def checkChemicalOverdue(request: WSGIRequest):
#     account: Account = request.user.account
#     orders = getOrder(CSOrder, CSOrder.STATUS.WAITING, account)
#     if orders == None: orders
#     try:
#         week    = DT.date.today() - DT.timedelta(days=7)
#         orders  = orders.filter(dateWithdraw__lt=week)
#         for order in orders:
#             cancelOrder(order)
#     except Exception as ex:
#         print(ex)
#         print("----------------------------------------")

class AuthenticationMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'base/login.html')
        return super().dispatch(request, *args, **kwargs)
    
class LabWebView(AuthenticationMixin):

    def get(self, request, *args, **kwargs):
        checkOverdue(request)
        # checkChemicalOverdue(request)

    def post(self, request, *args, **kwargs):
        checkOverdue(request)
        # checkChemicalOverdue(request)

class AdminMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'base/login.html')
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notFoundPage'))
        return super().dispatch(request, *args, **kwargs)

class AdminWebView(AdminMixin):

    def get(self, request, *args, **kwargs):
        checkOverdue(request)
        # checkChemicalOverdue(request)

    def post(self, request, *args, **kwargs):
        checkOverdue(request)
        # checkChemicalOverdue(request)

class AdminOnly(AdminWebView):
    def __init__(self) -> None:
        self.context = {}

class MenuList(LabWebView):
    def __init__(self) -> None:
        self.nameNotiBorrowing = 'แจ้งเตือนการยืม-คืนอุปกรณ์'
        self.nameScientificInstrument = 'แจ้งเตือนการจองเครื่องมือ'
        self.context = {}
        self.context['menuUpList'] = [
            { 'name': 'หน้าแรก', 'link': '/', 'icon': 'home', 'active': False },
        ]
        self.context['menuDownList'] = [
            { 'name': 'ติดต่อผู้ให้บริการ', 'link': '/contact', 'icon': 'help', 'active': False },
        ]

    def setMenuHome(self) -> list:
        self.context['menuList'] = [
        { 'name': 'ยืม-คืนอุปกรณ์วิทยาศาสตร์', 'link': 'equipment/list', 'image': 'static/images/landing/1.png' },
        { 'name': 'จองใช้งานเครื่องมือวิทยาศาสตร์', 'link': 'scientificInstrument/list', 'image': 'static/images/landing/2.png' },
        { 'name': 'เบิกใช้สารเคมีวิทยาศาสตร์', 'link': 'chemicalSubstance/list', 'image': 'static/images/landing/3.png' },
    ]

    def addMenuPage(self, category: int, active: int) -> list:
        self.nameNotification = None
        if category == 0:
            self.setBorrowingMenu()
        if category == 1:
            self.setBookingMenu()
        if category == 2:
            self.setWithdrawMenu()
        menuUpList: list = self.context['menuUpList']
        if active != None and active >= 0 and len(menuUpList) > active:
            menuUpList[active]['active'] = True
        self.setMenuDown(active)

    def setMenuDown(self, active: int):
        menuDownList: list = self.context['menuDownList']
        menuDownList.insert(0, { 'name': self.nameNotification, 'link': 'notifications', 'icon': 'notifications', 'active': False },)
        if active == -1:
            menuDownList[0]['active'] = True

    def setBorrowingMenu(self):
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameNotiBorrowing
        menuUpList.extend([
            { 'name': 'รายการอุปกรณ์', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ตะกร้าของฉัน', 'link': 'borrowing', 'icon': 'shopping_basket', 'active': False },
            { 'name': 'ประวัติการยืม-คืนอุปกรณ์', 'link': 'history', 'icon': 'history', 'active': False },
            { 'name': 'วิเคราะห์ข้อมูล', 'link': 'analysis', 'icon': 'assessment', 'active': False },
            ])

    def setBookingMenu(self):
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameScientificInstrument
        menuUpList.extend([
            { 'name': 'รายการเครื่องมือวิทยาศาตร์', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ปฏิทินการจอง', 'link': 'calendar', 'icon': 'shopping_basket', 'active': False },
            { 'name': 'วิเคราะห์ข้อมูล', 'link': 'analysis', 'icon': 'assessment', 'active': False },
            ])

    def setWithdrawMenu(self):
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameScientificInstrument
        menuUpList.extend([
            { 'name': 'รายการสารเคมี', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ประวัติการเบิกใช้สารเคมี', 'link': 'history', 'icon': 'history', 'active': False },
            { 'name': 'วิเคราะห์ข้อมูล', 'link': 'analysis', 'icon': 'assessment', 'active': False },
            ])