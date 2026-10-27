from django.test import TestCase
from django.contrib.auth import get_user_model
from inventory.models import Branch
from .models import Sale

class SaleModelTests(TestCase):
    def test_sale_starts_as_draft(self):
        user = get_user_model().objects.create_user(username="cashier", password="test-password-123")
        branch = Branch.objects.create(code="TEST", name="Sucursal de prueba")
        sale = Sale.objects.create(branch=branch, cashier=user)
        self.assertEqual(sale.status, Sale.Status.DRAFT)
