from django.conf import settings
from django.db import models

class AuditEvent(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT)
    action = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100, blank=True)
    summary = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    # Avoid storing passwords, tokens, full prescription details, or unnecessary patient data here.

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Evento de auditoría"
        verbose_name_plural = "Eventos de auditoría"

    def __str__(self):
        return f"{self.action} · {self.entity_type} · {self.created_at:%Y-%m-%d %H:%M}"
