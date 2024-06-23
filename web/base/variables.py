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
    "0": "ไม่ระบุ",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
}
BRANCH = {
    "B-Ed_Chemistry": "สาขาวิชาเคมี (คบ.)",
    "B-S_Chemistry": "สาขาวิชาเคมี (วท.บ.)",
    "B-Ed_Physical": "สาขาวิชาฟิสิกส์ (คบ.)",
    "B-S_Physical": "สาขาวิชาฟิสิกส์ (วท.บ.)",
    "B-Ed_Biology": "สาขาวิชาชีววิทยา (คบ.)",
    "B-S_Biology": "สาขาวิชาชีววิทยา (วท.บ.)",
    "Other_Other": "อื่น ๆ",
}

CATEGORY = {
    "student": "นักศึกษา",
    "teacher": "อาจารย์",
    "personnel": "บุคลากร",
    "other": "อื่นๆ",
    "NotSpecified": "ไม่ระบุ",
}