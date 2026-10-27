from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "apps.core"
    verbose_name = "Núcleo"

    def ready(self):
        from . import checks  # noqa: F401  registra los system checks
