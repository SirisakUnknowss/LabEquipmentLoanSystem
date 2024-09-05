# Django
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
# Project
from account.models import Account
from borrowing.models import Order

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

class AuthenticationMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'base/login.html')
        return super().dispatch(request, *args, **kwargs)
    
class LabWebView(AuthenticationMixin):

    def get(self, request, *args, **kwargs):
        self.status = request.user.account.status
        self.context['menuDownList'] = [
            { 'name': 'ติดต่อผู้ให้บริการ', 'link': '/contact', 'icon': 'help', 'active': False },
        ]
        checkOverdue(request)
        return redirect(reverse('notFoundPage'))
    def post(self, request, *args, **kwargs):
        self.status = request.user.account.status
        self.context['menuDownList'] = [
            { 'name': 'ติดต่อผู้ให้บริการ', 'link': '/contact', 'icon': 'help', 'active': False },
        ]
        checkOverdue(request)
        return redirect(reverse('notFoundPage'))

class AdminMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('homepage'))
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notFoundPage'))
        return super().dispatch(request, *args, **kwargs)

class AdminWebView(AdminMixin):

    def get(self, request, *args, **kwargs):
        return redirect(reverse('homepage'))

    def post(self, request, *args, **kwargs):
        return redirect(reverse('homepage'))

class AdminOnly(AdminWebView):
    def __init__(self) -> None:
        self.context = {}

class MenuList(LabWebView):
    def __init__(self) -> None:
        self.nameNoticeBorrowing = 'แจ้งเตือนการยืม-คืนอุปกรณ์'
        self.nameScientificInstrument = 'แจ้งเตือนการจองเครื่องมือ'
        self.nameChemicalSubstance = 'แจ้งเตือนการเบิกใช้สารเคมี'
        self.context = {}
        self.context['menuUpList'] = [
            { 'name': 'หน้าแรก', 'link': '/', 'icon': 'home', 'active': False },
        ]

    def setMenuHome(self) -> list:
        self.context['actionCategory'] = 'ใช้งานศูนย์'
        if self.status == Account.STATUS.ADMIN:
            self.context['menuDownList'].append({ 'name': 'ตั้งค่าผู้ใช้งาน', 'link': '/user/management', 'icon': 'settings', 'active': False })
        self.context['menuList'] = [
        { 'name': 'อุปกรณ์วิทยาศาสตร์', 'link': 'equipment/list', 'image': 'static/images/landing/1.png' },
        { 'name': 'เครื่องมือวิทยาศาสตร์', 'link': 'scientificInstrument/list', 'image': 'static/images/landing/2.png' },
        { 'name': 'สารเคมี', 'link': 'chemicalSubstance/list', 'image': 'static/images/landing/3.png' },
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
        if active != None and active >= 0 and len(menuUpList) >= active:
            if self.status == Account.STATUS.ADMIN and active > 1:
                active -= 1
            menuUpList[active]['active'] = True
        self.setMenuDown(active)

    def setMenuDown(self, active: int):
        menuDownList: list = self.context['menuDownList']
        menuDownList.insert(0, { 'name': self.nameNotification, 'link': 'notifications', 'icon': 'notifications', 'active': False },)
        if active == -1:
            menuDownList[0]['active'] = True
        if active == -2:
            menuDownList[0]['active'] = True

    def setBorrowingMenu(self):
        self.context['actionCategory']  = "ยืม - คืน"
        self.context['nameCategory']    = "อุปกรณ์"
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameNoticeBorrowing
        menuUpList.extend([
            { 'name': 'รายการอุปกรณ์', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ตะกร้าของฉัน', 'link': 'cart', 'icon': 'shopping_basket', 'active': False },
            { 'name': 'ประวัติการยืม-คืนอุปกรณ์', 'link': 'history', 'icon': 'history', 'active': False },
            ])
        if self.status == Account.STATUS.ADMIN:
            self.setMenuAdmin()

    def setBookingMenu(self):
        self.context['actionCategory']  = "จอง"
        self.context['nameCategory']    = "เครื่องมือ"
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameScientificInstrument
        menuUpList.extend([
            { 'name': 'รายการเครื่องมือวิทยาศาตร์', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ปฏิทินการจอง', 'link': 'calendar', 'icon': 'shopping_basket', 'active': False },
            { 'name': 'ประวัติการเบิกใช้สารเคมี', 'link': 'history', 'icon': 'history', 'active': False },
            ])
        if self.status == Account.STATUS.ADMIN:
            self.setMenuAdmin()

    def setWithdrawMenu(self):
        self.context['actionCategory']  = "เบิก"
        self.context['nameCategory']    = "สารเคมี"
        menuUpList: list = self.context['menuUpList']
        self.nameNotification = self.nameChemicalSubstance
        menuUpList.extend([
            { 'name': 'รายการสารเคมี', 'link': 'list', 'icon': 'description', 'active': False },
            { 'name': 'ตะกร้าของฉัน', 'link': 'cart', 'icon': 'shopping_basket', 'active': False },
            { 'name': 'ประวัติการเบิกใช้สารเคมี', 'link': 'history', 'icon': 'history', 'active': False },
            ])
        if self.status == Account.STATUS.ADMIN:
            self.setMenuAdmin()

    def setMenuAdmin(self):
        self.context['menuUpList'] = [item for item in self.context['menuUpList'] if item['name'] != "ตะกร้าของฉัน"]
        self.context['menuUpList'].append({ 'name': 'วิเคราะห์ข้อมูล', 'link': 'analysis', 'icon': 'assessment', 'active': False },)
        self.context['menuDownList'].append({ 'name': 'ตั้งค่าผู้ใช้งาน', 'link': '/user/management', 'icon': 'settings', 'active': False })
            