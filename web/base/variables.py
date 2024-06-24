STATUS_STYLE = {
    "waiting": {"style": "warning", "text": "รออนุมัติ"},
    "approved": {"style": "info", "text": "อนุมัติแล้ว"},
    "canceled": {"style": "danger", "text": "ยกเลิก"},
    "disapproved": {"style": "danger", "text": "คำขอล้มเหลว"},
    "completed": {"style": "success", "text": "คืนเรียบร้อยแล้ว"},
    "overdued": {"style": "danger", "text": "เกินกำหนดคืน"},
    "returned": {"style": "warning", "text": "คืนอุปกรณ์"},
}

UNIT = {
    "Millimeter": "mm",
    "Milliliter": "ml",
    "Centimeter": "cm",
    "Liter": "L",
    "Celsius": "℃",
    "CubicCentimeter": "cm³",
    "NotSpecified": "ไม่ระบุ",
    "Other": "อื่น ๆ",
}

DATE_TITLE = {
    "อุปกรณ์": "วันที่ยืม",
    "เครื่องมือ": "วันที่ใช้งาน",
    "สารเคมี": "วันที่เบิก",
}

LEVEL_CLASS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "0": "ไม่ระบุ",
}
BRANCH = {
    "B-Ed_Chemistry": "สาขาวิชาเคมี (คบ.)",
    "B-S_Chemistry": "สาขาวิชาเคมี (วท.บ.)",
    "B-Ed_Physical": "สาขาวิชาฟิสิกส์ (คบ.)",
    "B-S_Physical": "สาขาวิชาฟิสิกส์ (วท.บ.)",
    "B-Ed_Biology": "สาขาวิชาชีววิทยา (คบ.)",
    "B-S_Biology": "สาขาวิชาชีววิทยา (วท.บ.)",
    "other": "อื่น ๆ",
}

CATEGORY = {
    "student": "นักศึกษา",
    "teacher": "อาจารย์",
    "personnel": "บุคลากร",
    "other": "อื่นๆ",
    "notSpecified": "ไม่ระบุ",
}

PREFIX = {
    "Mr.": "นาย",
    "Mrs.": "นาง",
    "Miss": "นางสาว",
    "notSpecified": "ไม่ระบุ",
}

def addVariables(context: dict):
    context['BRANCH']       = BRANCH
    context['CATEGORY']     = CATEGORY
    context['LEVEL_CLASS']  = LEVEL_CLASS
    context['PREFIX']       = PREFIX
    return context