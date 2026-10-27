from decimal import Decimal

from django import template

register = template.Library()


@register.filter
def clp(value):
    """Formatea un monto como peso chileno: $1.234.567 (sin decimales)."""
    amount = Decimal(value).quantize(Decimal("1"))
    return "$" + f"{amount:,}".replace(",", ".")
