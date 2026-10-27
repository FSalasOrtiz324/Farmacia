from django.conf import settings
from django.core.checks import Error, Tags, register


@register(Tags.security, deploy=True)
def mock_integrations_forbidden(app_configs, **kwargs):
    """En `check --deploy` falla si algún adaptador externo está en modo simulado."""
    return [
        Error(
            f"{name}={getattr(settings, name)!r} es un modo simulado.",
            hint="Configure un adaptador autorizado o deshabilite la integración.",
            id="core.E001",
        )
        for name in settings.INTEGRATION_MODE_SETTINGS
        if "mock" in getattr(settings, name).lower()
    ]
