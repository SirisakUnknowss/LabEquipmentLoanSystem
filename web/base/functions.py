# Python
from csv import DictWriter
import os
import pandas as pd
#Django
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
    
def downloadFile(file_path, fileName):
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
    xlsxPath = os.path.join(dirPath, f"{fileName}.xlsx")
    convertCSVToXLSX(filePath, xlsxPath)
    return f"{fileName}.xlsx"

def convertCSVToXLSX(csvPath: str, xlsxPath: str):
    df = pd.read_csv(csvPath)
    df.to_excel(xlsxPath, index=False, engine='openpyxl')

def uploadImage(name, imageFile, model):
    if os.path.isfile(name):
        os.remove(name)
    fss         = FileSystemStorage()
    file        = fss.save(name, imageFile)
    file_url    = fss.url(file)
    model.image = file_url
    model.save(update_fields=['image'])

def convertToFloat(value) -> float:
    if value == '' or value == None or value == 'None': return 0.0
    try:
        return float(value)
    except:
        return 0.0

def checkTextBlank(value):
    if value == '' or value == 'None':return None
    return value

def writeFileExcel(dataList: list, header: dict, fileName: str):
    csvPath = f'{fileName}.csv'
    excelPath = f'{fileName}.xlsx'
    with open(csvPath, 'w', newline='', encoding='utf-8') as outfile:
        writer = DictWriter(outfile, fieldnames=header.keys())
        writer.writerow(header)
        writer.writerows(dataList)
    convertCSVToXLSX(csvPath, excelPath)
    return downloadFile(excelPath, excelPath)

def checkTextNone(value):
    if value == '' or value == 'None' or value == None:return ''
    return value

def exportAccountData(accounts, fileName):
    header      = { 'number': 'ลำดับ', 'studentID': 'รหัสนักศึกษา', 'name': 'ชื่อ', 'branch': 'สาขา', 'email': 'email',
                   'category': 'สถานะ' }
    accountList = []
    number      = 1
    for account in accounts:
        category = account.category
        if category == 'notSpecified':
            category = account.categoryOther
        accountList.append(
        {
            'number': number,
            'studentID': f'{account.studentID}',
            'name': f'{checkTextNone(account.firstname)} {checkTextNone(account.lastname)}',
            'branch': account.branch,
            'email': account.email,
            'category': f'{category}',
        })
        number += 1
    return writeFileExcel(accountList, header, fileName)