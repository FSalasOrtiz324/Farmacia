from django.test import TestCase
from .models import Product

class ProductModelTests(TestCase):
    def test_product_string(self):
        product = Product.objects.create(internal_code="TEST-001", name="Producto de prueba")
        self.assertIn("Producto de prueba", str(product))
