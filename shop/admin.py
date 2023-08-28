from django.contrib import admin

# Register your models here.
from .models import Product, Shop_Contact, Orders, OrderUpdate
admin.site.register(Product)
admin.site.register(Shop_Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
