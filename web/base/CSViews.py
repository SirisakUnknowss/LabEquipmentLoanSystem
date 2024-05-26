# Django
from django.db.models import Q
from django.core import serializers
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_framework.request import Request
# Project
from account.models import Account
from base.menu import AdminOnly, MenuList
from base.variables import STATUS_STYLE
from chemicalSubstance.models import ChemicalSubstance, HazardCategory, Order, ChemicalSubstanceCart
from chemicalSubstance.serializers import SlzChemicalSubstanceOutput, SlzHazardCategory

class ListPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, 1)
        results                     = ChemicalSubstance.objects.all().order_by('name')
        resultsJson                 = serializers.serialize("json", results)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = "/api/chemicalSubstance/remove"
        return render(request, 'pages/chemicalSubstance/listPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(2, 1)
        nameSearch                  = request.POST['nameSearch']
        name                        = Q(name__contains=nameSearch)
        results                     = ChemicalSubstance.objects.filter(name).order_by('name')
        resultsJson                 = serializers.serialize("json", results)
        self.context['results']     = results
        self.context['resultsJson'] = resultsJson
        self.context['deleteUrl']   = "/api/chemicalSubstance/remove"
        return render(request, 'pages/chemicalSubstance/listPage.html', self.context)

class DetailPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        return redirect(reverse('chemicalSubstanceListPage'))

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(0, None)
        try:
            order                       = Order.objects.get(id=request.POST['id'])
            self.context['order']       = order
            self.context['orders']      = order.chemicalSubstance.all()
            self.context['statusMap']   = STATUS_STYLE
            return render(request, 'pages/chemicalSubstance/detailPage.html', self.context)
        except Order.DoesNotExist:
            return redirect(reverse('chemicalSubstanceListPage'))

class CartPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, 2)
        self.context['carts']       = ChemicalSubstanceCart.objects.filter(user=request.user.account)
        self.context['status']      = "carts"
        self.context['deleteUrl']   = "/api/chemicalSubstance/cart/remove"
        return render(request, 'pages/chemicalSubstance/cartPage.html', self.context)

class WithdrawHistoryView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, 3)
        self.context = getOrder(1, request.user.account, self.context)
        return render(request, 'pages/chemicalSubstance/historyPage.html', self.context)

class AddPageView(AdminOnly):

    def get(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).get(request)
        ghsList                     = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.GHS)
        # unList                      = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.UN)
        self.context['ghsList']     = SlzHazardCategory(ghsList, many=True).data
        # self.context['unList']      = SlzHazardCategory(unList, many=True).data
        self.context['confirmUrl']  = '/api/chemicalSubstance/add'
        self.context['titleBar']    = 'เพิ่มสารเคมี'
        return render(request, 'pages/chemicalSubstance/addPage.html', self.context)

class EditPageView(AdminOnly):

    def post(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).post(request)
        try:
            ghsList                     = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.GHS)
            # unList                      = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.UN)
            instance                    = get_object_or_404(ChemicalSubstance, id=request.POST['id'])
            self.context['ghsList']     = SlzHazardCategory(ghsList, many=True).data
            # self.context['unList']      = SlzHazardCategory(unList, many=True).data
            self.context['result']      = SlzChemicalSubstanceOutput(instance).data
            self.context['confirmUrl']  = '/api/chemicalSubstance/edit'
            self.context['titleBar']    = 'แก้ไขสารเคมี'
            return render(request, 'pages/chemicalSubstance/addPage.html', self.context)
        except Http404:
            return redirect(reverse('chemicalSubstanceListPage'))
        
def getOrder(status: int, account: Account, context: dict):
    waiting     = Q(status=Order.STATUS.WAITING)
    canceled    = Q(status=Order.STATUS.CANCELED)
    approved    = Q(status=Order.STATUS.APPROVED)
    disapproved = Q(status=Order.STATUS.DISAPPROVED)
    if status == 0:
        orders = Order.objects.filter(waiting)
    if status == 1:
        orders = Order.objects.filter(disapproved | canceled | approved)
    if account.status == Account.STATUS.USER:
        orders = orders.filter(user=account)
    context['orders']      = orders
    context['statusMap']   = STATUS_STYLE
    return context

class NotificationsPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, -1)
        self.context = getOrder(0, request.user.account, self.context)
        return render(request, 'pages/chemicalSubstance/notificationPage.html', self.context)

class AnalysisView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        return redirect(reverse('chemicalSubstanceListPage'))
        super(MenuList, self).get(request)
        self.addMenuPage(2, 3)
        self.context['orders']      = []
        self.context['accounts']    = []
        self.context['equipments']  = []
        return render(request, 'pages/chemicalSubstance/analysisPage.html', self.context)