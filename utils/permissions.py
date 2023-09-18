from rest_framework.permissions import (BasePermission,)

class SupplierPermssion(BasePermission):
    def has_permission(self, request, view):
        if request.user.role=='Supplier':
            return True
        return False
    
class CustomerPermssion(BasePermission):
    def has_permission(self, request, view):
        if request.user.role=='Customer':
            return True
        return False
    

