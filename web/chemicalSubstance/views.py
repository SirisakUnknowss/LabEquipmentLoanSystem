# Django
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
# Project
from base.functions import uploadImage, convertToFloat, checkTextBlank
from base.views import LabAPIView
from chemicalSubstance.functions import updateHazard, updateImage
from chemicalSubstance.models import ChemicalSubstance
from chemicalSubstance.serializers import SlzChemicalSubstanceInput, SlzChemicalSubstance

class AddChemicalSubstance(LabAPIView):
    queryset            = ChemicalSubstance.objects.all()
    serializer_class    = SlzChemicalSubstanceInput
    permission_classes  = [ IsAuthenticated, IsAdminUser ]

    def post(self, request: Request, *args, **kwargs):
        try:
            checkList               = request.data.getlist(request.data['hazardCategory'])
            serializerInput         = self.get_serializer(data=request.data)
            serializerInput.is_valid(raise_exception=True)
            chemicalSubstance       = self.perform_create(serializerInput.validated_data, checkList)
            serializerOutput        = SlzChemicalSubstance(chemicalSubstance)
            self.response["result"] = serializerOutput.data
            return redirect(reverse('chemicalSubstanceListPage'))
        except Exception as ex:
            print("AddChemicalSubstance == " + ex)
            return redirect(reverse('chemicalSubstanceAddPage'))
    
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
            return redirect(reverse('chemicalSubstanceListPage'))
        chemicalSubstance = self.chemicalSubstances.first()
        name = self.request.POST.get('name')
        if name != self.chemicalSubstances.first().name:
            try:
                chemicalSubstance = ChemicalSubstance.objects.get(name=name)
                return redirect(reverse('chemicalSubstanceListPage'))
            except ChemicalSubstance.DoesNotExist:
                pass
        chemicalSubstance = self.update(chemicalSubstance)
        checkList = self.request.POST.getlist(self.request.POST.get('hazardCategory'))
        chemicalSubstance = updateHazard(chemicalSubstance, checkList)
        return redirect(reverse('chemicalSubstanceListPage'))

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
        return redirect(reverse('chemicalSubstanceListPage'))