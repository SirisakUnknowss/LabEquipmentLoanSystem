# Python
import os
import pandas as pd
#Django
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from equipment.models import getClassPath
    
def download_file(file_path, fileName):
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{fileName}"'
    response['Content-Type'] = 'application/octet-stream'
    return response

def getDataFile(dirPath: str, fileName: str, dataCls, queryset):
    if not(os.path.exists(dirPath)):
        os.makedirs(dirPath)
    fileRes     = f"{fileName}.csv"
    filePath    = os.path.join(dirPath, fileRes)
    dataset = dataCls().export(queryset=queryset)
    with open(filePath, "w") as f:
        f.write(dataset.csv)
    df = pd.read_csv(filePath)
    xlsxPath = os.path.join(dirPath, f"{fileName}.xlsx")
    df.to_excel(xlsxPath, index=False, engine='openpyxl')
    return f"{fileName}.xlsx"

def uploadImage(name, imageFile, model):
    fss         = FileSystemStorage()
    file        = fss.save(name, imageFile)
    file_url    = fss.url(file)
    model.image = file_url
    model.save(update_fields=['image'])