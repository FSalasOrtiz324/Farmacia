# Farmacia Chile — base inicial

Base de desarrollo para un sistema de gestión de farmacia. **No está lista para producción** y no emite documentos tributarios, no consulta recetas oficiales ni valida medicamentos controlados. Esos procesos requieren confirmación normativa e integración autorizada.

## Stack
- Python 3.12+
- Django 5.2 LTS
- PostgreSQL en entornos compartidos; SQLite solo para desarrollo inicial
- Plantillas Django + Bootstrap CDN para la interfaz inicial

## 1. Crear entorno (Debian 12)
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
cd farmacia_base
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations catalog inventory sales audit
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Abrir `http://127.0.0.1:8000/`.

Si aún no tienes `sudo`, ejecuta la instalación como `root` o pide habilitarlo; no trabajes como root para ejecutar la aplicación habitualmente.

## 2. Qué incluye esta primera base
- Proyecto Django configurado para variables de entorno.
- Catálogo de productos con código interno, código de barras, principio activo, concentración, forma farmacéutica y registro sanitario como dato de referencia.
- Lotes por producto con vencimiento, costo y estado.
- Movimientos de inventario auditables.
- Estructura inicial de ventas y líneas.
- Registro de auditoría.
- Admin de Django para cargar y revisar datos.
- Página de inicio y pruebas mínimas de modelos.

## 3. Decisiones de seguridad
- El inventario no debe modificarse silenciosamente: registrar movimientos.
- Las ventas se implementarán con transacciones atómicas y control de concurrencia.
- No se debe inferir la categoría legal de un medicamento a partir de su nombre. La clasificación debe verificarse con una fuente oficial.
- No conectar SII, recetas, pagos, convenios ni sistemas de medicamentos controlados con endpoints inventados.
- No introducir datos reales de pacientes en esta base de prueba.

## 4. Siguiente orden de trabajo
1. Revisar requisitos con la farmacia y confirmar roles/sucursales.
2. Completar catálogo y recepción de compras por lote.
3. Implementar movimientos FEFO con bloqueo de filas y pruebas de concurrencia.
4. Implementar caja/POS con totales y medios de pago.
5. Incorporar flujos de recetas y dispensación después de validar requisitos.
6. Diseñar adaptadores para SII y proveedores, con credenciales de prueba oficiales.
7. Pruebas de seguridad, respaldo, restauración y despliegue.

## 5. Comandos útiles
```bash
python manage.py check
python manage.py test
python manage.py makemigrations
python manage.py migrate
```
