# Django
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.request import Request
# Project
from base.menu import AdminOnly
from base.views import *
from chemicalSubstance.models import ChemicalSubstance, HazardCategory
from chemicalSubstance.serializers import SlzChemicalSubstance, SlzHazardCategory


class ListPageView(MenuList):

    def get(self, request: Request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, 1)
        results                     = ChemicalSubstance.objects.all().order_by('name')
        self.context['results']     = results
        self.context['deleteUrl']   = "/api/chemicalSubstance/remove"
        return render(request, 'pages/chemicalSubstance/listPage.html', self.context)

    def post(self, request: Request, *args, **kwargs):
        super(MenuList, self).post(request)
        self.addMenuPage(2, 1)
        name                        = Q(name__contains=request.POST['id_name'])
        results                     = ChemicalSubstance.objects.filter(name).order_by('name')
        self.context['results']     = results
        self.context['deleteUrl']   = "/api/chemicalSubstance/remove"
        return render(request, 'pages/chemicalSubstance/listPage.html', self.context)

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

    def get(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).get(request)
        return redirect(reverse('chemicalSubstanceListPage'))

    def post(self, request: Request, *args, **kwargs):
        super(AdminOnly, self).post(request)
        try:
            ghsList                     = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.GHS)
            # unList                      = HazardCategory.objects.filter(category=HazardCategory.CATEGORY.UN)
            id                          = request.POST['ChemicalSubstanceID']
            instance                    = get_object_or_404(ChemicalSubstance, id=id)
            self.context['ghsList']     = SlzHazardCategory(ghsList, many=True).data
            # self.context['unList']      = SlzHazardCategory(unList, many=True).data
            self.context['result']      = SlzChemicalSubstance(instance).data
            self.context['confirmUrl']  = '/api/chemicalSubstance/edit'
            self.context['titleBar']    = 'เพิ่มสารเคมี'
            return render(request, 'pages/chemicalSubstance/addPage.html', self.context)
        except Http404:
            return redirect(reverse('chemicalSubstanceListPage'))


class NotificationsPageView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, -1)
        self.context['orders'] = []
        return render(request, 'pages/chemicalSubstance/notificationPage.html', self.context)
class WithdrawHistoryView(MenuList):

    def get(self, request, *args, **kwargs):
        super(MenuList, self).get(request)
        self.addMenuPage(2, 2)
        self.context['orders'] = []
        return render(request, 'pages/chemicalSubstance/historyPage.html', self.context)

class AnalysisView(MenuList):

    def get(self, request, *args, **kwargs):
        return redirect(reverse('chemicalSubstanceListPage'))
        super(MenuList, self).get(request)
        self.addMenuPage(2, 3)
        self.context['orders']      = []
        self.context['accounts']    = []
        self.context['equipments']  = []
        return render(request, 'pages/chemicalSubstance/analysisPage.html', self.context)