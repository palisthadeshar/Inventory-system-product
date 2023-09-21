from django.contrib import admin
from apps.accounts.models import (User, Customer, Supplier,OTP)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'phone']
    


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id']
    
    
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['id']

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user','otp']