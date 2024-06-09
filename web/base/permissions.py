from rest_framework.permissions import BasePermission
from account.models import Account

class IsAdminAccount(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated):
            return False
        return request.user.account.status == Account.STATUS.ADMIN