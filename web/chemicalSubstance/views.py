# Django
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
# Project
from base.functions import convertToFloat, checkTextBlank
from account.models import Account
from base.views import LabAPIView
from chemicalSubstance.functions import updateHazard, updateImage, updateStatusOrder, cancelOrder
from chemicalSubstance.models import ChemicalSubstance, Order
from chemicalSubstance.serializers import SlzChemicalSubstanceInput, SlzChemicalSubstance, SlzApprovalInput, SlzCancelInput, SlzConfirmWithdrawalInput

class AddChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstanceInput
    permission_classes  = [ IsAuthenticated, IsAdminUser ]

    def post(self, request: Request, *args, **kwargs):
        try:
            checkList               = request.data.getlist(request.data['hazardCategory'])
            serializerInput         = SlzChemicalSubstanceInput(data=request.data)
            if not serializerInput.is_valid():
                self.response["error"] = next(iter(serializerInput.errors.values()))[0]
                return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
            chemicalSubstance       = self.perform_create(serializerInput.validated_data, checkList)
            self.response["result"] = '/chemicalSubstance/list'
            return Response(self.response)
        except Exception as ex:
            print("AddChemicalSubstance == " + ex)
            self.response["error"] = f"{ex}"
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def perform_create(self, validated: dict, checkList: list):
        chemicalSubstance = ChemicalSubstance(
            name                = validated.get("name"),
            serialNumber        = validated.get("serialNumber"),
            casNo               = validated.get("casNo"),
            place               = validated.get("place"),
            initialQuantity     = validated.get("initialQuantity"),
            remainingQuantity   = validated.get("remainingQuantity"),
            unit                = validated.get("unit"),
            catalogNo           = validated.get("catalogNo"),
            manufacturer        = validated.get("manufacturer"),
            distributor         = validated.get("distributor"),
            grade               = validated.get("grade"),
            price               = convertToFloat(validated.get("price")),
            hazardCategory      = validated.get("hazardCategory"),
            buyInDate           = validated.get("buyInDate"),
            activateDate        = validated.get("activateDate"),
            expirationDate      = validated.get("expirationDate"),
        )
        chemicalSubstance.save()
        chemicalSubstance = updateHazard(chemicalSubstance, checkList)
        chemicalSubstance = updateImage(chemicalSubstance, validated.get('name'), self.request.FILES)
        return chemicalSubstance

class EditChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstance
    permission_classes  = [ IsAuthenticated, IsAdminUser ]

    def post(self, request: Request, *args, **kwargs):
        self.chemicalSubstances = ChemicalSubstance.objects.filter(id=request.POST["chemicalSubstanceID"])
        if not self.chemicalSubstances.exists():
            # return redirect(reverse('chemicalSubstanceListPage'))
            self.response["result"] = '/chemicalSubstance/edit'
            return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        chemicalSubstance = self.chemicalSubstances.first()
        name = self.request.POST.get('name')
        if name != self.chemicalSubstances.first().name:
            try:
                chemicalSubstance = ChemicalSubstance.objects.get(name=name)
                self.response["result"] = '/chemicalSubstance/edit'
                return Response(self.response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                # return redirect(reverse('chemicalSubstanceListPage'))
            except ChemicalSubstance.DoesNotExist:
                pass
        chemicalSubstance = self.update(chemicalSubstance)
        checkList = self.request.POST.getlist(self.request.POST.get('hazardCategory'))
        chemicalSubstance = updateHazard(chemicalSubstance, checkList)
        self.response["result"] = '/chemicalSubstance/list'
        return Response(self.response)
        # return redirect(reverse('chemicalSubstanceListPage'))

    def update(self, cs: ChemicalSubstance) -> ChemicalSubstance:
        data                    = self.request.POST
        name                    = checkTextBlank(data.get("name"))
        cs.name                 = name
        cs.serialNumber         = checkTextBlank(data.get("serialNumber"))
        cs.casNo                = checkTextBlank(data.get("casNo"))
        cs.place                = checkTextBlank(data.get("place"))
        cs.initialQuantity      = convertToFloat(data.get("initialQuantity"))
        cs.remainingQuantity    = convertToFloat(data.get("remainingQuantity"))
        cs.unit                 = checkTextBlank(data.get("unit"))
        cs.catalogNo            = checkTextBlank(data.get("catalogNo"))
        cs.manufacturer         = checkTextBlank(data.get("manufacturer"))
        cs.distributor          = checkTextBlank(data.get("distributor"))
        cs.grade                = checkTextBlank(data.get("grade"))
        cs.price                = convertToFloat(data.get("price"))
        cs.hazardCategory       = checkTextBlank(data.get("hazardCategory"))
        cs.buyInDate            = checkTextBlank(data.get("buyInDate"))
        cs.activateDate         = checkTextBlank(data.get("activateDate"))
        cs.expirationDate       = checkTextBlank(data.get("expirationDate"))
        cs.save()
        cs = updateImage(cs, name, self.request.FILES)
        return cs

class RemoveChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstance
    permission_classes  = [ IsAuthenticated, IsAdminUser ]

    def post(self, request: Request, *args, **kwargs):
        ChemicalSubstance.objects.filter(id=request.POST.get('deleteID')).delete()
        self.response["result"] = '/chemicalSubstance/list'
        return Response(self.response)

class ApprovalChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzApprovalInput
    permission_classes  = [ IsAuthenticated, IsAdminUser ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzApprovalInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order   = serializerInput.validated_data['orderID']
        statusStr: str      = serializerInput.validated_data['status']
        self.updateApprover()
        updateStatusOrder(self.order, statusStr)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

    def updateApprover(self):
        account: Account = self.request.user.account
        self.order.approver = account
        self.order.save(update_fields=["approver"])

class CancelChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzCancelInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request: Request, *args, **kwargs):
        serializerInput = SlzCancelInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
            return Response(self.response, status=status.HTTP_400_BAD_REQUEST)
        self.order: Order   = serializerInput.validated_data['orderID']
        cancelOrder(self.order)
        self.response["result"] = 'Update Completed.'
        return Response(self.response)

class ConfirmWithdrawalApi(LabAPIView):
    queryset            = Order.objects.all()
    serializer_class    = SlzConfirmWithdrawalInput
    permission_classes  = [ IsAuthenticated ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        serializerInput = SlzConfirmWithdrawalInput(data=request.data)
        if not serializerInput.is_valid():
            self.response["error"] = next(iter(serializerInput.errors.values()))[0]
        self.response["result"] = serializerInput.data
        return Response(self.response)
        # equipments  = EquipmentCart.objects.filter(user=account)
        # if not equipments.exists():
        #     return redirect(reverse('addScientificInstrumentPage'))
        # order = Order.objects.create(user=account)
        # for item in equipments:
        #     equipment = Equipment.objects.get(id=item.equipment.id)
        #     if equipment.quantity < item.quantity:
        #         return redirect(reverse('addScientificInstrumentPage'))
        #     equipment.quantity -= item.quantity
        #     equipment.save()
        #     borrowing = Borrowing.objects.create(user=account, equipment=item.equipment, quantity=item.quantity)
        #     order.equipment.add(borrowing)
        # equipments.delete()
        # return redirect(reverse('notificationsEquipmentPage'))