from django.contrib import admin
from .models import Sale, SaleLine

class SaleLineInline(admin.TabularInline):
    model = SaleLine
    extra = 0

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("id", "branch", "cashier", "status", "total", "created_at")
    list_filter = ("status", "branch", "created_at")
    inlines = [SaleLineInline]
    readonly_fields = ("subtotal", "discount_total", "total", "created_at", "completed_at", "tax_document_status")
