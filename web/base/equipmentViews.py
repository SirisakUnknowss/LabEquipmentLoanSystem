# Django
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
# Project
from base.views import *

class NotificationsPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, -1)
        self.context['orders'] = self.getOrders(request.user.account)
        return render(request, 'pages/equipments/notifications_page.html', self.context)

    def getOrders(self, account: Account):
        # orders = Order.objects.filter(user=account, status=Order.STATUS.OVERDUED)
        orders = Order.objects.filter(user=account)
        # if account.status == Account.STATUS.ADMIN:
        #     returned    = Q(status=Order.STATUS.RETURNED)
        #     waiting     = Q(status=Order.STATUS.WAITING)
        #     overdued    = Q(status=Order.STATUS.OVERDUED)
        #     orders      = Order.objects.filter(waiting | returned | overdued)
        return orders

# class InformationEquipmentView(MenuList):

#     def get(self, request, *args, **kwargs):
#         super(MenuList, self).get(request)
#         self.addMenuPage(0, 3)
#         waiting     = Q(status=Order.STATUS.WAITING)
#         approved    = Q(status=Order.STATUS.APPROVED)
#         returned    = Q(status=Order.STATUS.RETURNED)
#         orders      = Order.objects.filter(waiting | approved | returned)
#         if request.user.account.status == Account.STATUS.USER:
#             orders  = orders.filter(user=request.user.account)
#         self.context['orders'] = orders
#         return render(request, 'pages/equipments/information_page.html', self.context)

class BorrowingHistoryView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 3)
        canceled    = Q(status=Order.STATUS.CANCELED)
        completed   = Q(status=Order.STATUS.COMPLETED)
        disapproved = Q(status=Order.STATUS.DISAPPROVED)
        orders      = Order.objects.filter(disapproved | canceled | completed)
        if request.user.account.status == Account.STATUS.USER:
            orders  = orders.filter(user=request.user.account)
        self.context['orders'] = orders
        return render(request, 'pages/equipments/borrowing_history_page.html', self.context)

class AddPageView(MenuList):

    def get(self, request, *args, **kwargs):
        if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        return render(request, 'pages/equipments/add_equipment.html', self.context)

    def post(self, request, *args, **kwargs):
        if not(request.user.is_authenticated) or request.user.account.status != Account.STATUS.ADMIN:
            return redirect(reverse('homepage'))
        self.addMenuPage(0, 1)
        equipmentID = request.POST['EquipmentID']
        equipment = Equipment.objects.filter(id=equipmentID)
        if equipment.exists():
            self.context['equipment'] = equipment.first()
            return render(request, 'pages/equipments/add_equipment.html', self.context)
        return redirect(reverse('equipmentListPage'))

class ListPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(0, 1)
        equipments = Equipment.objects.all().order_by('name')
        equipmentsJson = serializers.serialize("json", equipments)
        self.context['equipments'] = equipments
        self.context['equipmentsJson'] = equipmentsJson
        return render(request, 'pages/equipments/listPage.html', self.context)

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, 1)
        nameEquipment   = request.POST['nameequipment']
        name            = Q(name__contains=nameEquipment)
        equipments      = Equipment.objects.filter(name).order_by('name')
        equipmentsJson  = serializers.serialize("json", equipments)
        self.context['equipments'] = equipments
        self.context['equipmentsJson'] = equipmentsJson
        return render(request, 'pages/equipments/listPage.html', self.context)

class DetailPageView(MenuList):
    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        return redirect(reverse('equipmentListPage'))

    def post(self, request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, None)
        status      = request.POST['StatusBorrowing']
        equipmentID = request.POST['EquipmentID']
        try:
            order   = Order.objects.get(id=equipmentID, status=status)
            self.context['order'] = order
            self.context['status'] = status
            return render(request, 'pages/equipments/equipment_detail_page.html', self.context)
        except ObjectDoesNotExist:
            return redirect(reverse('equipmentListPage'))

class CartListPageView(MenuList):
    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        equipmentsCart = EquipmentCart.objects.filter(user=request.user.account)
        self.addMenuPage(0, 2)
        self.context['equipmentsCart'] = equipmentsCart
        return render(request, 'pages/equipments/cart_equipment_page.html', self.context)