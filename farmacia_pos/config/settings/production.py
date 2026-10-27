from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F403
from .base import INTEGRATION_MODE_SETTINGS, SECRET_KEY, env_bool

DEBUG = False
if env_bool("DEBUG", False):
    raise ImproperlyConfigured("DEBUG no puede estar activo en producción.")
if "replace-me" in SECRET_KEY or len(SECRET_KEY) < 50:
    raise ImproperlyConfigured("SECRET_KEY de producción ausente o insegura.")

for _name in INTEGRATION_MODE_SETTINGS:
    if "mock" in globals()[_name].lower():
        raise ImproperlyConfigured(f"{_name} usa un adaptador simulado; prohibido en producción.")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
