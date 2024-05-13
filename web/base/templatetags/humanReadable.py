#Python
from datetime import datetime
# DJANGO
from django import template

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