from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from catalog.models import Product

class Branch(models.Model):
    code = models.CharField("Código", max_length=20, unique=True)
    name = models.CharField("Sucursal", max_length=120)
    address = models.CharField("Dirección", max_length=240, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.name

class StockLot(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Disponible"
        QUARANTINE = "QUARANTINE", "Cuarentena"
        DAMAGED = "DAMAGED", "Dañado"
        RECALLED = "RECALLED", "Retirado / alerta"

    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="lots")
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="lots")
    lot_number = models.CharField("Número de lote", max_length=100)
    expiry_date = models.DateField("Vencimiento", null=True, blank=True)
    quantity = models.PositiveIntegerField("Cantidad disponible", default=0)
    unit_cost = models.DecimalField("Costo unitario", max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["expiry_date", "lot_number"]
        constraints = [
            models.UniqueConstraint(fields=["product", "branch", "lot_number"], name="unique_product_branch_lot"),
        ]
        verbose_name = "Lote de inventario"
        verbose_name_plural = "Lotes de inventario"

    def __str__(self):
        return f"{self.product.name} · Lote {self.lot_number} · {self.branch.name}"

class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        RECEIPT = "RECEIPT", "Recepción"
        SALE = "SALE", "Venta"
        RETURN = "RETURN", "Devolución"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"
        TRANSFER_IN = "TRANSFER_IN", "Entrada por traslado"
        TRANSFER_OUT = "TRANSFER_OUT", "Salida por traslado"
        QUARANTINE = "QUARANTINE", "Cuarentena"

    lot = models.ForeignKey(StockLot, on_delete=models.PROTECT, related_name="movements")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity_delta = models.IntegerField("Cambio de unidades")
    reason = models.CharField(max_length=240)
    reference = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Movimiento de inventario"
        verbose_name_plural = "Movimientos de inventario"

    def __str__(self):
        return f"{self.lot} ({self.quantity_delta:+})"
