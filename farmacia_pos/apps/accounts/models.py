from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Usuario propio desde la primera migración (AUTH-01).

    Los roles y el ámbito por sucursal se agregan en AUTH-02/AUTH-03. Los usuarios
    no se eliminan: se desactivan (`is_active=False`) para conservar la trazabilidad.
    """

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
