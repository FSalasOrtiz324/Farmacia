# Farmacia POS — Chile

Sistema POS y de administración para una farmacia en Chile. **Está en desarrollo y no tiene ninguna certificación**: no emite documentos tributarios, no procesa pagos reales y no valida recetas.
Hoja de ruta: `PLAN_MAESTRO.md`. Requisitos originales: `docs/requirements/`.

## Stack
Python 3.14 · Django 6.1.2 · PostgreSQL 18 · Django Templates + Bootstrap 5 + HTMX · dependencias fijadas en `uv.lock`.

## Puesta en marcha (desarrollo)
```bash
pip install --user uv            # una vez
uv sync                          # crea .venv con versiones del lockfile
cp .env.example .env
podman compose up -d db          # o: docker compose up -d db  (PostgreSQL 18 en puerto 5433)
uv run python manage.py migrate
uv run python manage.py runserver
```

## Maquetas de interfaz
Pantallas navegables con datos ficticios y sin backend, en **http://127.0.0.1:8000/maquetas/**.
Solo existen cuando `DEBUG=true`. Código en `apps/mockups/`.

| Pantalla | Qué muestra |
|---|---|
| Login | Usuario, contraseña y sucursal; 2FA para cuentas privilegiadas (`admin.demo`, `qf.demo`) |
| Inicio | Indicadores, alertas de vencimiento, cuarentena y reconciliación, estado de integraciones |
| POS / Caja | Carrito interactivo: lector o código (Enter), F2 buscar, F9 pagar, Esc descartar, bloqueo por receta, pago mixto y vuelto |
| Ventas | Estados separados de venta, pago y documento; detalle con trazabilidad lote → receta → pago |
| Devoluciones | Vinculadas a la venta original; destino del producto (cuarentena, vendible o baja) separado del reintegro; nota de crédito simulada |
| Catálogo | Ficha con producto, fabricante y titular separados, condición de venta con fuente y validador, proveedores |
| Inventario | Stock por lote (FEFO y semáforo de vencimientos), kardex inmutable, ajuste con motivo y aprobación |
| Transferencias | Estados borrador → despachada → en tránsito → recibida; diferencias registradas explícitamente |
| Compras | Órdenes de compra y recepción con diferencias, lote y vencimiento obligatorios |
| Recetas | Acceso restringido, validación, libro de controlados |
| Caja y turnos | Turnos, arqueo con diferencia calculada |
| Convenios | Quién financia el beneficio, forma de validación, montos por recuperar |
| Reportes | Venta bruta, descuentos, devoluciones y neta; margen con costo histórico |
| Administración | Usuarios y roles, 2FA, adaptadores (sin secretos), auditoría |

### Exportar como sitio estático (GitHub Pages)
```bash
uv run python manage.py export_mockups ../farmacia-maquetas
```
Genera una carpeta por pantalla con enlaces relativos. La entrada al sitio es la pantalla de login.

## Comandos
```bash
uv run python manage.py test --settings=config.settings.test
uv run ruff check . && uv run ruff format --check .
```
