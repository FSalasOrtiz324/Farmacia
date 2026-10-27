from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("internal_code", "name", "barcode", "active_ingredient", "is_active")
    search_fields = ("internal_code", "barcode", "name", "active_ingredient")
    list_filter = ("is_active", "requires_prescription", "dosage_form")
