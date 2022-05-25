from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import F
#Project
from base.views import LabAPIGetView
from .models import EquipmentCart
from .serializers import SlzEquipmentCartInput, SlzEquipmentCart

# Create your views here.

class AddItemForBorrowingApi(LabAPIGetView):
    queryset            = EquipmentCart.objects.all()
    serializer_class    = SlzEquipmentCartInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account                 = request.user.account
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        equipment               = self.perform_create(serializerInput, account)
        serializerOutput        = SlzEquipmentCart(equipment)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('equipment-list'))
    
    def perform_create(self, serializer, account):
        validated = serializer.validated_data
        equipmentCart = EquipmentCart.objects.filter(user=account, equipment=validated.get("equipment"))
        if equipmentCart.exists():
            equipmentCart.update(quantity=F('quantity') + validated.get("quantity"))
            return equipmentCart
        equipmentCart = EquipmentCart(
            user        = account,
            equipment   = validated.get("equipment"),
            quantity    = validated.get("quantity"),
            )
        equipmentCart.save()
        return equipmentCart

class RemoveItemForBorrowingApi(LabAPIGetView):
    queryset            = EquipmentCart.objects.all()
    serializer_class    = SlzEquipmentCart
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account     = request.user.account
        idCart      = request.data['equipmentCart']
        EquipmentCart.objects.filter(id=idCart, user=account).delete()
        return redirect(reverse('equipmentcart-list'))
