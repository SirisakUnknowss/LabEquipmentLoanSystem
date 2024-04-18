
from base.functions import uploadImage
from chemicalSubstance.models import ChemicalSubstance, HazardCategory, getClassPath

def updateHazard(chemicalSubstance: ChemicalSubstance, checkList: list) -> ChemicalSubstance:
    chemicalSubstance.ghs.clear()
    chemicalSubstance.unClass.clear()
    for data in checkList:
        query = HazardCategory.objects.get(serialNumber=data)
        if chemicalSubstance.hazardCategory == 'unClass':
            chemicalSubstance.unClass.add(query)
        if chemicalSubstance.hazardCategory == 'ghs':
            chemicalSubstance.ghs.add(query)
    chemicalSubstance.save()
    return chemicalSubstance

def updateImage(chemicalSubstance: ChemicalSubstance, name: str, file: dict) -> ChemicalSubstance:
    if not(file.get('upload', False)):
        return chemicalSubstance
    upload      = file.get('upload')
    namePath    = getClassPath(chemicalSubstance, name)
    uploadImage(namePath, upload, chemicalSubstance)
    return chemicalSubstance
