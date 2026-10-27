from django.contrib import admin
from .models import Branch, StockLot, StockMovement

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active")
    search_fields = ("code", "name")

@admin.register(StockLot)
class StockLotAdmin(admin.ModelAdmin):
    list_display = ("product", "branch", "lot_number", "expiry_date", "quantity", "status")
    search_fields = ("product__name", "product__internal_code", "lot_number")
    list_filter = ("branch", "status", "expiry_date")

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("lot", "movement_type", "quantity_delta", "reason", "created_by", "created_at")
    list_filter = ("movement_type", "created_at")
    readonly_fields = ("lot", "movement_type", "quantity_delta", "reason", "reference", "created_by", "created_at")
    def has_add_permission(self, request):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
