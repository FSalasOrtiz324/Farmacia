"""Vistas de maqueta: solo renderizan datos ficticios, sin lógica de negocio ni escritura."""

import json

from django.http import Http404
from django.shortcuts import render

from . import data

SCREENS = {
    "inicio": ("Inicio", "bi-house"),
    "pos": ("POS / Caja", "bi-cart"),
    "ventas": ("Ventas", "bi-receipt"),
    "catalogo": ("Catálogo", "bi-capsule"),
    "historial": ("Historial de cierres", "bi-calendar-check"),
}
# Pantallas fuera del menú lateral.
STANDALONE = {"login": "Iniciar sesión"}


def _products():
    return [
        {
            **p,
            "condition_label": data.CONDITIONS[p["condition"]][0],
            "condition_color": data.CONDITIONS[p["condition"]][1],
        }
        for p in data.PRODUCTS
    ]


def screen(request, slug="inicio"):
    if slug not in SCREENS and slug not in STANDALONE:
        raise Http404
    products = _products()
    context = {
        "screens": SCREENS,
        "slug": slug,
        "title": SCREENS[slug][0] if slug in SCREENS else STANDALONE[slug],
        "branch": data.BRANCH,
        "user_demo": data.USER,
        "products": products,
        "sales": data.SALES,
        "today": data.TODAY,
        "closings_json": json.dumps(
            [{**c, "total": int(c["total"])} for c in data.CLOSINGS]
        ),
        "low_stock": [p for p in products if p["stock"] <= 5],
        "pos_catalog_json": json.dumps(
            [
                {
                    "sku": p["sku"],
                    "ean": p["ean"],
                    "name": p["name"],
                    "presentation": p["presentation"],
                    "price": int(p["price"]),
                    "stock": p["stock"],
                    "condition": p["condition"],
                }
                for p in products
            ]
        ),
    }
    return render(request, f"mockups/{slug}.html", context)
