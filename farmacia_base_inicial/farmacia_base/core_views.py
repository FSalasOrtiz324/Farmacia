from django.shortcuts import render
from catalog.models import Product
from inventory.models import StockLot

def home(request):
    context = {
        "product_count": Product.objects.filter(is_active=True).count(),
        "lot_count": StockLot.objects.count(),
        "low_stock_lots": StockLot.objects.filter(status=StockLot.Status.AVAILABLE, quantity__lte=5).count(),
    }
    return render(request, "home.html", context)
