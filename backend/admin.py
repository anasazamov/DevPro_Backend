from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Admin panelidagi ustunlar
    search_fields = ('name',)  # Qidiruv maydoni
    list_filter = ('stock',)  # Filtrlar

admin.site.register(Product, ProductAdmin)
