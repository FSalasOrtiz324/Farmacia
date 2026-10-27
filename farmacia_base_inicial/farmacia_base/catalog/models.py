from django.db import models

class Product(models.Model):
    class DosageForm(models.TextChoices):
        TABLET = "TABLET", "Comprimido"
        CAPSULE = "CAPSULE", "Cápsula"
        SYRUP = "SYRUP", "Jarabe"
        CREAM = "CREAM", "Crema"
        DROPS = "DROPS", "Gotas"
        INJECTABLE = "INJECTABLE", "Inyectable"
        OTHER = "OTHER", "Otro"

    internal_code = models.CharField("Código interno", max_length=40, unique=True)
    barcode = models.CharField("Código de barras", max_length=80, blank=True, db_index=True)
    name = models.CharField("Nombre comercial", max_length=200, db_index=True)
    active_ingredient = models.CharField("Principio activo / DCI", max_length=200, blank=True)
    concentration = models.CharField("Concentración", max_length=100, blank=True)
    dosage_form = models.CharField("Forma farmacéutica", max_length=20, choices=DosageForm.choices, default=DosageForm.OTHER)
    presentation = models.CharField("Presentación", max_length=160, blank=True)
    route = models.CharField("Vía de administración", max_length=80, blank=True)
    sanitary_registration = models.CharField("Registro sanitario (referencia)", max_length=100, blank=True)
    requires_prescription = models.BooleanField("Requiere receta (por verificar)", default=False)
    is_active = models.BooleanField("Activo", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"{self.name} ({self.internal_code})"
