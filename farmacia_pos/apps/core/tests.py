import os
import subprocess
import sys

from django.conf import settings
from django.core.checks import run_checks
from django.test import SimpleTestCase, override_settings


class MockIntegrationGuardTests(SimpleTestCase):
    def test_deploy_check_rejects_mock_modes(self):
        errors = run_checks(include_deployment_checks=True)
        self.assertIn("core.E001", {e.id for e in errors})

    @override_settings(
        PAYMENT_MODE="provider",
        TAX_DOCUMENT_MODE="provider",
        PRESCRIPTION_INTEGRATION_MODE="manual",
    )
    def test_deploy_check_accepts_non_mock_modes(self):
        errors = run_checks(include_deployment_checks=True)
        self.assertNotIn("core.E001", {e.id for e in errors})

    def _import_production(self, **overrides):
        env = {
            **os.environ,
            "SECRET_KEY": "x" * 60,
            "DEBUG": "false",
            "PAYMENT_MODE": "provider",
            "TAX_DOCUMENT_MODE": "provider",
            "PRESCRIPTION_INTEGRATION_MODE": "manual",
            **overrides,
        }
        return subprocess.run(  # noqa: S603
            [sys.executable, "-c", "import config.settings.production"],
            env=env,
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True,
        )

    def test_production_settings_load_without_mocks(self):
        result = self._import_production()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_production_settings_refuse_mock_payment(self):
        result = self._import_production(PAYMENT_MODE="mock")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PAYMENT_MODE", result.stderr)

    def test_production_settings_refuse_debug(self):
        result = self._import_production(DEBUG="true")
        self.assertNotEqual(result.returncode, 0)

    def test_production_settings_refuse_weak_secret(self):
        result = self._import_production(SECRET_KEY="replace-me-for-local-development-only")
        self.assertNotEqual(result.returncode, 0)
