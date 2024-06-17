# Django
from django.db.models import Q
from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.request import Request
# Project
from account.models import Account
from base.menu import MenuList, AdminOnly
from base.variables import STATUS_STYLE
from borrowing.models import EquipmentCart, Order
from equipment.models import Equipment
        
def getOrder(status: int, account: Account, context: dict):
    completed   = Q(status=Order.STATUS.COMPLETED)
    canceled    = Q(status=Order.STATUS.CANCELED)
    approved    = Q(status=Order.STATUS.APPROVED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    if status == 0:
        orders = Order.objects.exclude(disapproved | canceled | approved | completed)
    if status == 1:
        orders = Order.objects.filter(disapproved | canceled | approved | completed)
    if account.status == Account.STATUS.USER:
        orders = orders.filter(user=account)
    context['orders']      = orders
    context['statusMap']   = STATUS_STYLE
    return context

class NotificationsPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, -1)
        self.context = getOrder(0, request.user.account, self.context)
        return render(request, 'pages/equipments/notificationPage.html', self.context)

class BorrowingHistoryView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 3)
        self.context = getOrder(1, request.user.account, self.context)
        return render(request, 'pages/equipments/borrowingHistoryPage.html', self.context)

class AddPageView(AdminOnly):

    def get(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).get(request)
        self.context['titleBar']    = 'เพิ่มเครื่องมือวิทยาศาตร์'
        self.context['confirmUrl']  = '/api/equipment/add'
        return render(request, 'pages/equipments/addPage.html', self.context)

class EditPageView(AdminOnly):

    def post(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).post(request)
        try:
            result                      = Equipment.objects.get(id=request.POST['id'])
            self.context['result']      = result
            self.context['titleBar']    = 'แก้ไขเครื่องมือวิทยาศาตร์'
            self.context['confirmUrl']  = '/api/equipment/edit'
            return render(request, 'pages/equipments/addPage.html', self.context)
        except Equipment.DoesNotExist:
            return redirect(reverse('equipmentListPage'))

class ListPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 1)
        results                     = Equipment.objects.all().order_by('name')
        resultsJson                 = serializers.serialize("json", results)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = '/api/equipment/remove'
        return render(request, 'pages/equipments/listPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, 1)
        nameSearch                  = request.POST['nameSearch']
        name                        = Q(name__contains=nameSearch)
        results                     = Equipment.objects.filter(name).order_by('name')
        resultsJson                 = serializers.serialize("json", results)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = '/api/equipment/remove'
        return render(request, 'pages/equipments/listPage.html', self.context)

class DetailPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        return redirect(reverse('equipmentListPage'))

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, None)
        try:
            order                       = Order.objects.get(id=request.POST['id'])
            self.context['order']       = order
            self.context['equipments']  = order.equipment.all()
            self.context['statusMap']   = STATUS_STYLE
            return render(request, 'pages/equipments/detailPage.html', self.context)
        except Order.DoesNotExist:
            return redirect(reverse('equipmentListPage'))

class CartPageView(MenuList):
    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
        self.addMenuPage(0, 2)
        self.context['equipments']  = equipmentsCart
        self.context['status']      = "borrowing"
        return render(request, 'pages/equipments/cartPage.html', self.context)

class AnalysisView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        if request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('notFoundPage'))
        self.addMenuPage(0, 4)
        self.context['orders']      = self.orderAll()
        self.context['accounts']    = self.accountAll()
        self.context['equipments']  = self.topEquipment()
        return render(request, 'pages/equipments/analysisPage.html', self.context)

    def topEquipment(self):
        equipments = Equipment.objects.all().order_by('-statistics').filter(statistics__gt=1)[:20]
        return equipments
        
    def accountAll(self):
        admin               = Q(status=Account.STATUS.ADMIN)
        user                = Q(status=Account.STATUS.USER)
        account             = dict()
        accounts            = Account.objects.all()
        account['all']      = accounts.count()
        account['user']     = accounts.filter(user).count()
        account['admin']    = accounts.filter(admin).count()
        return account

    def orderAll(self):
        waiting     = Q(status=Order.STATUS.WAITING)
        approved    = Q(status=Order.STATUS.APPROVED)
        overdue     = Q(status=Order.STATUS.OVERDUED)
        returned    = Q(status=Order.STATUS.RETURNED)
        canceled    = Q(status=Order.STATUS.CANCELED)
        completed   = Q(status=Order.STATUS.COMPLETED)
        disapproved = Q(status=Order.STATUS.DISAPPROVED)
        order       = dict()
        orders      = Order.objects.all()

        order['all']            = orders.count()
        order['waiting']        = orders.filter(waiting).count()
        order['canceled']       = orders.filter(canceled).count()
        order['returned']       = orders.filter(returned).count()
        order['approved']       = orders.filter(approved).count()
        order['overdued']       = orders.filter(overdue).count()
        order['completed']      = orders.filter(completed).count()
        order['disapproved']    = orders.filter(disapproved).count()
        return order