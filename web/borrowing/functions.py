# Python
from datetime import datetime, timedelta
#Project
from account.models import Account
from borrowing.models import Borrowing, Order

def updateStatusOrder(order: Order, status):
    if not order == None and status in Order.STATUS:
        order.status = status
        order.save(update_fields=["status"])

def updateStatistics(order: Order):
    for equipment in order.equipment.all():
        borrowing : Borrowing = equipment
        borrowing.equipment.statistics += 1
        borrowing.equipment.save(update_fields=["statistics"])

def updateApprover(order: Order, account: Account):
    if order.status != Order.STATUS.APPROVED: return
    updateStatistics(order)
    order.approver     = account
    order.dateApproved = datetime.now()
    order.dateReturn   = datetime.now() + timedelta(days=7)
    order.save(update_fields=["approver", "dateApproved", "dateReturn"])

def returnEquipments(order: Order):
    updateStatusOrder(order, Order.STATUS.COMPLETED)
    for equipment in order.equipment.all():
        borrowing : Borrowing = equipment
        borrowing.equipment.quantity += borrowing.quantity
        borrowing.equipment.save(update_fields=["quantity"])

def borrowingAgain(order: Order):
    updateStatusOrder(order, Order.STATUS.WAITING)
    order.dateBorrowing = datetime.now()
    order.approver      = None
    order.dateApproved  = None
    order.dateReturn    = None
    order.save(update_fields=["dateBorrowing", "approver", "dateApproved", "dateReturn"])