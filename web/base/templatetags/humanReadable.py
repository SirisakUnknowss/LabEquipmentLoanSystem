#Python
from datetime import datetime
# DJANGO
from django import template
# Project
from base.variables import UNIT, DATE_TITLE

register = template.Library()

@register.filter
def DateFormatter(value):
    try:
        dateFormat = "%Y-%m-%dT%H:%M:%SZ"
        dateTime = datetime.strptime(value, dateFormat)
        return dateTime.strftime("%d-%m-%Y %I:%M %p")
    except:
        return "None"

@register.filter
def AddComma(value):
	try:
		value = int(value)
		value = "{}".format(f"{value:,d}")
		return value
	except:
		return 0

@register.filter
def hash(h, key):
    try:
        return h[key]
    except:
        return None

@register.filter
def Unit(value):
	try:
		return UNIT[value]
	except:
		return 0

@register.filter
def dateTitleNotice(value):
	try:
		return DATE_TITLE[value]
	except:
		return None