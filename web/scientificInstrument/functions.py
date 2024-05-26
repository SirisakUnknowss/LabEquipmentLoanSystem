# Project
from borrowing.models import Order
from scientificInstrument.models import Booking, ScientificInstrument

def updateStatusOrder(order: Booking, status):
    if not order == None and status in Order.STATUS:
        if status == Order.STATUS.APPROVED:
            updateStatistics(order.scientificInstrument)
        order.status = status
        order.save(update_fields=["status"])

def updateStatistics(scientificInstrument: ScientificInstrument):
    scientificInstrument.statistics += 1
    scientificInstrument.save(update_fields=["statistics"])