"""Datos ficticios para las maquetas. No representan productos, personas ni precios reales."""

from decimal import Decimal as D

BRANCH = "Sucursal Demo Centro"
USER = {"name": "Cajero Demo", "role": "Cajero"}

PRODUCTS = [
    {
        "sku": "DEMO-0001",
        "ean": "7800000000011",
        "name": "Paracetamol Demo 500 mg",
        "presentation": "Caja 16 comprimidos",
        "lab": "Laboratorio Ficticio A",
        "condition": "VD",
        "price": D("1990"),
        "stock": 42,
        "status": "Activo",
    },
    {
        "sku": "DEMO-0002",
        "ean": "7800000000028",
        "name": "Ibuprofeno Demo 400 mg",
        "presentation": "Caja 20 comprimidos",
        "lab": "Laboratorio Ficticio B",
        "condition": "VD",
        "price": D("2490"),
        "stock": 3,
        "status": "Activo",
    },
    {
        "sku": "DEMO-0003",
        "ean": "7800000000035",
        "name": "Amoxicilina Demo 500 mg",
        "presentation": "Caja 21 cápsulas",
        "lab": "Laboratorio Ficticio A",
        "condition": "R",
        "price": D("4590"),
        "stock": 18,
        "status": "Activo",
    },
    {
        "sku": "DEMO-0004",
        "ean": "7800000000042",
        "name": "Producto Controlado Demo",
        "presentation": "Caja 30 comprimidos",
        "lab": "Laboratorio Ficticio C",
        "condition": "RCH",
        "price": D("8990"),
        "stock": 6,
        "status": "Activo",
    },
    {
        "sku": "DEMO-0005",
        "ean": "7800000000059",
        "name": "Insulina Demo",
        "presentation": "Frasco 10 mL (cadena de frío)",
        "lab": "Laboratorio Ficticio D",
        "condition": "RR",
        "price": D("15990"),
        "stock": 4,
        "status": "Pendiente de validar",
    },
    {
        "sku": "DEMO-0006",
        "ean": "7800000000066",
        "name": "Crema Hidratante Demo",
        "presentation": "Tubo 100 g",
        "lab": "Laboratorio Ficticio B",
        "condition": "VD",
        "price": D("5490"),
        "stock": 0,
        "status": "Activo",
    },
]

CONDITIONS = {
    "VD": ("Venta directa", "success"),
    "R": ("Receta simple", "warning"),
    "RR": ("Receta retenida", "orange"),
    "RCH": ("Receta cheque", "danger"),
}

LOTS = [
    {
        "product": "Paracetamol Demo 500 mg",
        "lot": "L-A101",
        "expiry": "2026-12-15",
        "days": 52,
        "warehouse": "Sala de ventas",
        "qty": 12,
        "status": "Disponible",
    },
    {
        "product": "Paracetamol Demo 500 mg",
        "lot": "L-A145",
        "expiry": "2027-08-30",
        "days": 310,
        "warehouse": "Sala de ventas",
        "qty": 30,
        "status": "Disponible",
    },
    {
        "product": "Ibuprofeno Demo 400 mg",
        "lot": "L-B220",
        "expiry": "2027-02-01",
        "days": 100,
        "warehouse": "Sala de ventas",
        "qty": 3,
        "status": "Disponible",
    },
    {
        "product": "Amoxicilina Demo 500 mg",
        "lot": "L-A330",
        "expiry": "2026-11-20",
        "days": 27,
        "warehouse": "Bodega",
        "qty": 18,
        "status": "Disponible",
    },
    {
        "product": "Insulina Demo",
        "lot": "L-D010",
        "expiry": "2027-04-10",
        "days": 168,
        "warehouse": "Refrigerador 1",
        "qty": 4,
        "status": "Cuarentena",
    },
    {
        "product": "Crema Hidratante Demo",
        "lot": "L-B901",
        "expiry": "2026-10-01",
        "days": -23,
        "warehouse": "Bodega",
        "qty": 2,
        "status": "Vencido",
    },
    {
        "product": "Producto Controlado Demo",
        "lot": "L-C077",
        "expiry": "2027-06-30",
        "days": 249,
        "warehouse": "Gabinete controlados",
        "qty": 6,
        "status": "Disponible",
    },
]

MOVEMENTS = [
    {
        "when": "24-10-2026 09:12",
        "type": "Recepción",
        "product": "Paracetamol Demo 500 mg",
        "lot": "L-A145",
        "qty": "+30",
        "user": "Bodega Demo",
        "ref": "REC-0012",
    },
    {
        "when": "24-10-2026 10:40",
        "type": "Venta",
        "product": "Ibuprofeno Demo 400 mg",
        "lot": "L-B220",
        "qty": "-2",
        "user": "Cajero Demo",
        "ref": "V-000231",
    },
    {
        "when": "24-10-2026 11:05",
        "type": "Cuarentena",
        "product": "Insulina Demo",
        "lot": "L-D010",
        "qty": "0 (estado)",
        "user": "QF Demo",
        "ref": "CUA-0003",
    },
    {
        "when": "24-10-2026 11:30",
        "type": "Ajuste (conteo)",
        "product": "Crema Hidratante Demo",
        "lot": "L-B901",
        "qty": "-1",
        "user": "Bodega Demo",
        "ref": "CNT-0007",
    },
]

SALES = [
    {
        "id": "V-000231",
        "when": "24-10-2026 10:40",
        "cashier": "Cajero Demo",
        "total": D("4980"),
        "sale": "Confirmada",
        "payment": "Aprobado",
        "tax": "Pendiente (simulado)",
    },
    {
        "id": "V-000230",
        "when": "24-10-2026 10:22",
        "cashier": "Cajero Demo",
        "total": D("13580"),
        "sale": "Confirmada",
        "payment": "Aprobado",
        "tax": "Aceptado (simulado)",
    },
    {
        "id": "V-000229",
        "when": "24-10-2026 09:58",
        "cashier": "Cajero Demo 2",
        "total": D("1990"),
        "sale": "Confirmada",
        "payment": "Desconocido",
        "tax": "A reconciliar",
    },
    {
        "id": "V-000228",
        "when": "23-10-2026 19:47",
        "cashier": "Cajero Demo 2",
        "total": D("8990"),
        "sale": "Devuelta parcial",
        "payment": "Reembolsado",
        "tax": "Con nota de crédito (simulado)",
    },
]

PURCHASE_ORDERS = [
    {
        "id": "OC-0045",
        "supplier": "Distribuidora Ficticia Norte",
        "date": "20-10-2026",
        "lines": 12,
        "total": D("845000"),
        "status": "Enviada",
    },
    {
        "id": "OC-0044",
        "supplier": "Droguería Demo Sur",
        "date": "18-10-2026",
        "lines": 5,
        "total": D("212400"),
        "status": "Recepción parcial",
    },
    {
        "id": "OC-0043",
        "supplier": "Distribuidora Ficticia Norte",
        "date": "10-10-2026",
        "lines": 20,
        "total": D("1320500"),
        "status": "Completa",
    },
]

RECEIPT_LINES = [
    {
        "product": "Paracetamol Demo 500 mg",
        "ordered": 30,
        "received": 30,
        "lot": "L-A145",
        "expiry": "2027-08-30",
        "cost": D("820"),
    },
    {
        "product": "Ibuprofeno Demo 400 mg",
        "ordered": 24,
        "received": 20,
        "lot": "",
        "expiry": "",
        "cost": D("1100"),
    },
    {
        "product": "Insulina Demo",
        "ordered": 6,
        "received": 4,
        "lot": "L-D010",
        "expiry": "2027-04-10",
        "cost": D("9800"),
    },
]

PRESCRIPTIONS = [
    {
        "folio": "RX-DEMO-0101",
        "type": "Receta simple",
        "origin": "Física",
        "date": "22-10-2026",
        "status": "Validada",
        "dispensed": "Total",
    },
    {
        "folio": "RX-DEMO-0102",
        "type": "Receta retenida",
        "origin": "Electrónica",
        "date": "23-10-2026",
        "status": "Pendiente de validar",
        "dispensed": "—",
    },
    {
        "folio": "RX-DEMO-0103",
        "type": "Receta cheque",
        "origin": "Física",
        "date": "24-10-2026",
        "status": "Rechazada",
        "dispensed": "—",
    },
]

AGREEMENTS = [
    {
        "name": "Convenio Empresa Ficticia",
        "funder": "Farmacia",
        "benefit": "10% en productos VD",
        "valid": "01-01-2026 a 31-12-2026",
        "validation": "Manual",
        "status": "Vigente",
    },
    {
        "name": "Programa Laboratorio Demo",
        "funder": "Tercero (laboratorio)",
        "benefit": "Precio pactado en 3 SKU",
        "valid": "01-06-2026 a 30-11-2026",
        "validation": "Pendiente de confirmar acceso",
        "status": "Borrador",
    },
]

SHIFTS = [
    {
        "register": "Caja 1",
        "cashier": "Cajero Demo",
        "opened": "24-10-2026 08:55",
        "float": D("50000"),
        "cash_sales": D("187400"),
        "status": "Abierta",
    },
    {
        "register": "Caja 2",
        "cashier": "Cajero Demo 2",
        "opened": "23-10-2026 14:00",
        "float": D("50000"),
        "cash_sales": D("96300"),
        "status": "Cerrada (diferencia -$500)",
    },
]

USERS = [
    {
        "username": "cajero.demo",
        "name": "Cajero Demo",
        "role": "Cajero",
        "branch": BRANCH,
        "active": True,
        "mfa": False,
    },
    {
        "username": "qf.demo",
        "name": "QF Demo",
        "role": "Químico farmacéutico / DT",
        "branch": BRANCH,
        "active": True,
        "mfa": True,
    },
    {
        "username": "bodega.demo",
        "name": "Bodega Demo",
        "role": "Bodega",
        "branch": BRANCH,
        "active": True,
        "mfa": False,
    },
    {
        "username": "admin.demo",
        "name": "Admin Demo",
        "role": "Administrador",
        "branch": "Todas",
        "active": True,
        "mfa": True,
    },
]

INTEGRATIONS = [
    {"name": "Pagos", "mode": "Simulado (mock)", "status": "Sin proveedor contratado"},
    {
        "name": "Documentos tributarios (SII)",
        "mode": "Simulado (mock)",
        "status": "Método de emisión por definir con contador",
    },
    {
        "name": "Receta electrónica (SNRE)",
        "mode": "Manual / simulado",
        "status": "Acceso no confirmado con MINSAL",
    },
    {"name": "Catálogo ISP", "mode": "Importación manual", "status": "Fuente por confirmar"},
]

# Día "de hoy" en la maqueta y cierres de caja de los días anteriores.
TODAY = {"date": "2026-10-24", "total": D("19550"), "sales": 3, "items": 7}
CLOSINGS = [
    {
        "date": f"2026-10-{day:02d}",
        "total": D(180000 + (day * 37813) % 160000),
        "sales": 40 + (day * 17) % 35,
        "items": 70 + (day * 29) % 60,
        "closed_by": "Cajero Demo",
        "closed_at": f"{20 + day % 2}:{(day * 7) % 60:02d}",
    }
    for day in range(1, 24)
    if day not in (4, 11, 18)  # domingos sin atención
]
