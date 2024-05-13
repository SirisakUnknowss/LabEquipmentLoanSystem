# Django
from django.core import serializers
from rest_framework.request import Request
# Project
from base.variables import STATUS_STYLE
from base.views import *

class NotificationsPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, -1)
        self.context['orders']      = self.getOrders(request.user.account)
        self.context['statusMap']   = STATUS_STYLE
        return render(request, 'pages/equipments/notificationsPage.html', self.context)

    def getOrders(self, account: Account):
        orders = Order.objects.filter(user=account)
        if account.status == Account.STATUS.ADMIN:
            canceled    = Q(status=Order.STATUS.CANCELED)
            disapproved = Q(status=Order.STATUS.DISAPPROVED)
            completed   = Q(status=Order.STATUS.COMPLETED)
            orders      = Order.objects.exclude(canceled | disapproved | completed)
        return orders

class BorrowingHistoryView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 3)
        self.context['orders']      = self.getOrders(request.user.account)
        self.context['statusMap']   = STATUS_STYLE
        return render(request, 'pages/equipments/borrowingHistoryPage.html', self.context)

    def getOrders(self, account: Account):
        canceled    = Q(status=Order.STATUS.CANCELED)
        completed   = Q(status=Order.STATUS.COMPLETED)
        disapproved = Q(status=Order.STATUS.DISAPPROVED)
        orders      = Order.objects.filter(disapproved | canceled | completed)
        if account.status == Account.STATUS.USER:
            orders  = orders.filter(user=account)
        return orders

class AddPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        return render(request, 'pages/equipments/addPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        self.addMenuPage(0, 1)
        equipmentID = request.POST['EquipmentID']
        equipment = Equipment.objects.filter(id=equipmentID)
        if equipment.exists():
            self.context['equipment'] = equipment.first()
            return render(request, 'pages/equipments/addPage.html', self.context)
        return redirect(reverse('equipmentListPage'))

class ListPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 1)
        equipments = Equipment.objects.all().order_by('name')
        equipmentsJson = serializers.serialize("json", equipments)
        self.context['equipments'] = equipments
        self.context['equipmentsJson'] = equipmentsJson
        return render(request, 'pages/equipments/listPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, 1)
        nameSearch      = request.POST['nameSearch']
        name            = Q(name__contains=nameSearch)
        equipments      = Equipment.objects.filter(name).order_by('name')
        equipmentsJson  = serializers.serialize("json", equipments)
        self.context['equipments'] = equipments
        self.context['equipmentsJson'] = equipmentsJson
        return render(request, 'pages/equipments/listPage.html', self.context)

class DetailPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        return redirect(reverse('equipmentListPage'))

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, None)
        status      = request.POST['StatusBorrowing']
        equipmentID = request.POST['EquipmentID']
        try:
            order                       = Order.objects.get(id=equipmentID, status=status)
            self.context['order']       = order
            self.context['equipments']  = order.equipment.all()
            self.context['status']      = status
            self.context['statusMap']   = STATUS_STYLE
            return render(request, 'pages/equipments/detailPage.html', self.context)
        except Order.DoesNotExist:
            return redirect(reverse('equipmentListPage'))

class CartListPageView(MenuList):
    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
        self.addMenuPage(0, 2)
        self.context['equipments']  = equipmentsCart
        self.context['status']      = "borrowing"
        return render(request, 'pages/equipments/cartEquipmentPage.html', self.context)