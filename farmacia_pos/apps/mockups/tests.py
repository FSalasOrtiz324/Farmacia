from django.test import TestCase, override_settings
from django.urls import clear_url_caches, reverse

from .views import SCREENS, STANDALONE


@override_settings(DEBUG=True)
class MockupScreensTests(TestCase):
    """Las urls de maquetas solo se registran con DEBUG=True (ver config/urls.py)."""

    def setUp(self):
        import importlib

        import config.urls

        clear_url_caches()
        importlib.reload(config.urls)

    def test_every_screen_renders_with_mock_banner(self):
        for slug in [*SCREENS, *STANDALONE]:
            with self.subTest(slug=slug):
                response = self.client.get(f"/maquetas/{slug}/")
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "MAQUETA")

    def test_unknown_screen_is_404(self):
        self.assertEqual(self.client.get("/maquetas/no-existe/").status_code, 404)

    def test_pos_never_calls_receipt_a_valid_boleta(self):
        response = self.client.get(reverse("mockups:screen", args=["pos"]))
        self.assertContains(response, "No es una boleta electrónica válida")

    def test_historial_lists_past_closings_and_inicio_offers_close(self):
        self.assertContains(self.client.get("/maquetas/historial/"), "2026-10-23")
        self.assertContains(self.client.get("/maquetas/inicio/"), "Cerrar caja del día")


class MockupsHiddenOutsideDebugTests(TestCase):
    def test_mockups_not_routed_when_debug_false(self):
        import importlib

        import config.urls

        clear_url_caches()
        importlib.reload(config.urls)
        self.assertEqual(self.client.get("/maquetas/").status_code, 404)
