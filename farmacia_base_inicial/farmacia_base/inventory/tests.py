from datetime import date
from django.test import TestCase
from catalog.models import Product
from .models import Branch, StockLot

class StockLotTests(TestCase):
    def test_lot_is_linked_to_product_and_branch(self):
        product = Product.objects.create(internal_code="MED-001", name="Producto")
        branch = Branch.objects.create(code="CENTRAL", name="Sucursal central")
        lot = StockLot.objects.create(product=product, branch=branch, lot_number="L-001", expiry_date=date(2027, 1, 1), quantity=10, unit_cost="1200.00")
        self.assertEqual(lot.quantity, 10)
