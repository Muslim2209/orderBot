from django.contrib import admin
from .models import Product, Order, Category, CartItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated', 'status']
    list_editable = ['status']
