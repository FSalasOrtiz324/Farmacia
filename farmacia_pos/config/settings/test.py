from .base import *  # noqa: F403

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # solo acelera los tests
PAYMENT_MODE = "mock"
TAX_DOCUMENT_MODE = "mock"
PRESCRIPTION_INTEGRATION_MODE = "manual_or_mock"
