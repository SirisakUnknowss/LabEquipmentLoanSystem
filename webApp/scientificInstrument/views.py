#Django
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import AllowAny
from django.urls import reverse
from django.shortcuts import redirect
from django.db.models import F
from rest_framework.exceptions import ValidationError
#Project
from base.views import LabListView, LabAPIGetView
from scientificInstrument.models import ScientificInstrument, getClassPath
from scientificInstrument.serializers import SlzScientificInstrumentInput, SlzScientificInstrument

# Create your views here.


class AddScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes  = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        serializerInput         = self.get_serializer(data=request.data)
        serializerInput.is_valid(raise_exception=True)
        scientificInstrument    = self.perform_create(serializerInput)
        serializerOutput        = SlzScientificInstrument(scientificInstrument)
        self.response["result"] = serializerOutput.data
        return redirect(reverse('scientific-instruments-list'))
    
    def perform_create(self, serializer):
        validated = serializer.validated_data
        scientificInstrument = ScientificInstrument.objects.filter(number=validated.get("number"))
        if scientificInstrument.exists():
            return scientificInstrument.first()
        else:
            scientificInstrument = ScientificInstrument(
                name        = validated.get("name"),
                number      = validated.get("number"),
                place       = validated.get("place"),
                detail      = validated.get("detail"),
                annotation  = validated.get("annotation"),
            )
            scientificInstrument.save()
            if not(self.request.FILES.get('upload', False)):
                return scientificInstrument
            upload      = self.request.FILES['upload']
            fss         = FileSystemStorage()
            name        = getClassPath(scientificInstrument, validated.get("name"))
            file        = fss.save(name, upload)
            file_url    = fss.url(file)
            scientificInstrument.image = file_url
            scientificInstrument.save()
            return scientificInstrument
        
class RemoveScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"]).delete()
        return redirect(reverse('scientific-instruments-list'))

class EditScientificInstrument(LabAPIGetView):
    queryset            = ScientificInstrument.objects.all()
    serializer_class    = SlzScientificInstrumentInput
    permission_classes = [ AllowAny ]

    def post(self, request, *args, **kwargs):
        account = request.user.account
        if account.status != "admin":
            raise ValidationError('Please login with admin account.')
        scientificInstrument = ScientificInstrument.objects.filter(id=request.POST["scientificInstrument"])
        if not scientificInstrument.exists():
            return redirect(reverse('scientific-instruments-list'))
        scientificInstrument.update(
            name        =request.POST["name"],
            number      = request.POST["number"],
            place       = request.POST["place"],
            detail      = request.POST["detail"],
            annotation  = request.POST["annotation"],
            )
        if not(request.FILES.get('upload', False)):
            return redirect(reverse('scientific-instruments-list'))
        scientificInstrument:ScientificInstrument = scientificInstrument[0]
        upload      = self.request.FILES['upload']
        fss         = FileSystemStorage()
        name        = getClassPath(scientificInstrument, request.POST["name"])
        file        = fss.save(name, upload)
        file_url    = fss.url(file)
        scientificInstrument.image = file_url
        scientificInstrument.save()
        return redirect(reverse('scientific-instruments-list'))