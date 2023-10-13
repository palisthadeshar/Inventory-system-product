from django.contrib import admin
from apps.products.models import Product,Sales

# Register your models here.
admin.site.register(Product)
admin.site.register(Sales)
