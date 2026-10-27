# Plan maestro de desarrollo — Sistema POS y administración para una farmacia en Chile

**Versión:** 1.0  
**Fecha:** 24 de octubre de 2026  
**Estado:** Plan previo a la programación; no es certificación legal, sanitaria ni tributaria.  
**Documento base:** *Análisis integral — Sistema POS y administración para una farmacia en Chile* (11 páginas, fechado 24-10-2026).

## Contenido

1. Decisión ejecutiva y stack recomendado
2. Qué aporta el PDF y qué queda pendiente
3. Alcance del producto y pantallas
4. Reglas de negocio no negociables
5. Estructura técnica sugerida del repositorio
6. Modelo de datos inicial
7. Flujos críticos antes del código
8. Backlog detallado por fases
9. Estrategia de pruebas y criterios de aceptación
10. Instrucciones para el agente de IA programador
11. Variables de configuración
12. Orden de entregas y puertas de control
13. Decisiones pendientes antes de producción
14. Fuentes y criterio final de éxito

\newpage

---

## 0. Decisión ejecutiva

### Producto que se construirá

Una aplicación web de gestión farmacéutica con POS integrado, inventario trazable por lote y vencimiento, compras y proveedores, caja, recetas/dispensaciones, documentación tributaria, convenios, reportes, seguridad y auditoría. Se empieza con una única farmacia/sucursal configurable, pero el modelo de datos debe soportar más de una sucursal desde el inicio.

### Stack recomendado

| Capa | Decisión | Razón |
|---|---|---|
| Lenguaje | Python 3.14.x | Productivo para reglas de negocio, integraciones y pruebas. Seleccionar la última microversión compatible y bloquearla en el entorno. |
| Backend | Django 6.1.x, parche estable vigente al comenzar | Autenticación, permisos, formularios, ORM, migraciones, sesiones y administración incorporados. La versión exacta debe quedar fijada en el lockfile. |
| Base de datos | PostgreSQL 18.x, parche soportado vigente | Transacciones, restricciones relacionales, bloqueos de filas y consistencia para inventario/ventas simultáneas. |
| Interfaz | Django Templates + Bootstrap 5 + HTMX | Interfaz responsive con pocas piezas móviles; evita necesitar un SPA complejo al inicio. |
| Contratos externos | Adaptadores Python por proveedor; cliente HTTP validado | Mantiene los módulos del negocio desacoplados de SII, SNRE, pagos y convenios. |
| Pruebas | `unittest`/`TestCase` de Django y pruebas de integración; añadir pytest solo si el equipo lo prefiere | Las pruebas deben formar parte de cada tarea, no dejarse para el final. |
| Calidad | Ruff para lint/formato; type hints en servicios críticos | Código consistente y errores detectables temprano. |
| Entorno local | Git + entorno virtual o Docker Compose | Reproducibilidad entre el computador del desarrollador y el agente de IA. |
| Producción | Linux, PostgreSQL, aplicación detrás de proxy TLS; servicio WSGI/ASGI según necesidad | Separación de configuración, secretos y datos de producción. No usar el servidor de desarrollo de Django en producción. |

**Regla de versiones:** antes de instalar, confirmar en la documentación oficial que la versión de Django seleccionada admite la versión menor de Python elegida. Fijar todas las dependencias en un archivo de bloqueo. No programar con versiones `latest` flotantes sin fijarlas.

### Arquitectura

**Monolito modular**, no microservicios inicialmente. El backend posee módulos bien separados, pero se despliega como una aplicación. Una API REST pública no es requisito para el primer MVP: las páginas internas pueden usar Django Templates/HTMX. Los adaptadores externos sí encapsulan las comunicaciones HTTP/API que se autoricen.

### Principio fundamental

Una venta, sus líneas, los pagos, la asignación de lotes, los movimientos de inventario, la dispensación (si corresponde) y el documento tributario deben quedar relacionados y poder auditarse. Las operaciones sensibles deben ser transaccionales o tener estados/reintentos explícitos para resolver fallos parciales sin duplicar cobros, movimientos ni documentos.

---

## 1. Qué aporta el PDF y qué queda pendiente

El PDF define el mapa funcional y los principales riesgos del proyecto. No contiene contratos API completos, credenciales, reglas definitivas de convenios, catálogo maestro descargable ni una especificación suficiente para activar una integración externa por sí sola.

| Área del PDF | Requisitos extraídos | Consecuencia en el proyecto |
|---|---|---|
| Flujo operativo (págs. 2–3) | Compra, recepción, almacenamiento, venta/dispensación, cobro/tributación y administración; trazabilidad de la operación completa. | Modelo relacional y eventos vinculados desde el diseño, no como campos sueltos. |
| Catálogo (pág. 3) | Separar principio activo/DCI, producto autorizado, presentación, lote, fabricante/laboratorio, titular del registro y proveedor. | No usar una sola tabla genérica `Producto` para todos los conceptos. |
| Inventario (pág. 4) | Stock por sucursal/lote; vencimientos; FEFO; mínimos/máximos; conteos; transferencias; cuarentena, retiros, cadena de frío, devoluciones e historial. | Kardex/movimientos inmutables y existencias calculadas/consistentes por lote y ubicación. |
| Recetas (pág. 5) | Venta directa, receta simple, retenida, receta cheque; registro de prescriptor/paciente cuando sea exigible; dispensaciones parciales; control especial de estupefacientes/psicotrópicos. | Motor de reglas regulado por clasificación autorizada; acceso restringido y registro detallado. No inferir la condición por el nombre del medicamento. |
| Convenios/CENABAST (pág. 6) | Reglas variables de elegibilidad, productos, vigencia, topes, acumulación, validación y liquidación; no asumir una API universal por RUT. | Motor de beneficios configurable más un adaptador/proceso por convenio. Diferenciar quién financia el descuento. |
| POS/SII (pág. 7) | Boleta, factura, notas de crédito/débito, guía si aplica, estados de envío, voucher según modelo tributario y conciliación. No duplicar documentos. | Capa tributaria independiente, con estados explícitos y reconciliación antes de reintentar un resultado incierto. |
| Integraciones (pág. 8) | SII, MINSAL/SNRE, ISP, CENABAST, entidades de convenios y operadores de pago. Acceso/credenciales deben confirmarse. | Stubs de desarrollo aislados de producción; no inventar endpoints ni simular respuestas como si fueran reales. |
| Administración (pág. 8) | Compras, pagos a proveedores, caja, precios, promociones, usuarios, permisos, reportes y auditoría. | Módulos de operación y administración; separar ventas, cobros, margen y cuentas por cobrar. |
| Seguridad/arquitectura (pág. 9) | Privilegios mínimos, autenticación robusta, cifrado, auditoría, respaldos, recuperación, exportaciones controladas; PostgreSQL y adaptadores externos. | Seguridad desde el inicio, secretos fuera del código y plan de recuperación probado. |
| Implementación/pruebas (pág. 10) | Etapas por catálogo/inventario, POS/tributación, recetas, convenios y validación; incluye casos de concurrencia y permisos. | Backlog por entregas con pruebas de aceptación obligatorias. |

### Límites de certeza

- El documento sirve como análisis y mapa de requisitos; no reemplaza validación del director técnico/químico farmacéutico, contador, asesor legal, SII, MINSAL, ISP ni SEREMI.
- La Ley 21.719 tiene vigencia anunciada para el 1 de diciembre de 2026; el sistema debe diseñarse desde el principio pensando en la protección de datos y validar las disposiciones vigentes al desplegar.
- El material ministerial hallado sobre SNRE es un documento de consulta pública de marzo de 2025. Describe APIs e interoperabilidad HL7 FHIR para sistemas privados acreditados, pero no demuestra por sí solo que este proyecto tenga acceso habilitado, credenciales, acreditación o un contrato aplicable. Eso debe confirmarse con MINSAL antes de construir el adaptador productivo.
- No se debe activar emisión tributaria real, pagos reales ni dispensación de productos regulados hasta disponer de especificaciones, credenciales, procedimientos aprobados y pruebas de certificación requeridas.

---

## 2. Alcance del producto

### 2.1 MVP técnico (entorno de desarrollo/pruebas)

Debe permitir recorrer de extremo a extremo una operación de prueba con datos ficticios:

1. iniciar sesión y aplicar un rol;
2. crear productos, presentaciones, proveedores y lotes;
3. recepcionar una compra e ingresar cantidades/costos/lotes/vencimientos;
4. consultar stock vendible y alertas de vencimiento;
5. abrir caja/turno;
6. crear una venta con varias líneas, calcular precios/descuentos y registrar un pago simulado;
7. reservar/asignar stock y registrar movimientos dentro de transacciones consistentes;
8. dejar el documento tributario como pendiente en el adaptador simulado, sin emitir documentos reales;
9. consultar historial, auditoría y reportes;
10. probar fallos, concurrencia, cancelaciones y restauración de respaldo.

### 2.2 Primera versión operativa (solo después de validar requisitos)

Incluirá catálogo autorizado, lotes reales, ventas, caja, compras, perfiles y permisos reales, trazabilidad, procedimientos de dispensación aprobados, documentos tributarios mediante un método autorizado, pagos con proveedor contratado y respaldos. Deben quedar fuera de producción las integraciones cuyo acceso no esté confirmado.

### 2.3 Módulos posteriores

- Integración SNRE acreditada y conforme a la documentación vigente.
- Integraciones con cada convenio/operador, CENABAST y catálogos autorizados del ISP cuando exista mecanismo autorizado.
- Reposición sugerida con históricos, estacionalidad, stock comprometido, vencimientos y plazo de proveedor.
- Multisucursal avanzado, transferencias entre locales y conciliación centralizada.
- Comercio electrónico/entrega a domicilio, solo si el negocio lo requiere y se evalúa aparte.

### 2.4 Fuera de alcance por defecto

- Prescribir medicamentos o tomar decisiones clínicas.
- Sustituir automáticamente un medicamento por compartir principio activo.
- Inferir diagnóstico, condición médica, afiliación o elegibilidad a partir del RUT.
- Guardar datos de tarjetas o CVV. Los pagos deben procesarse mediante terminal/proveedor autorizado; almacenar solo referencias, estados e importes mínimos necesarios.
- Declarar el sistema “certificado” o “cumplidor” sin las aprobaciones correspondientes.
- Usar APIs inventadas, ingeniería inversa, credenciales de terceros no autorizadas o scraping como supuesto reemplazo de una integración oficial.

### 2.5 Mapa mínimo de pantallas

- **Inicio / dashboard:** alertas urgentes, stock bajo, productos por vencer, estado de caja, errores de integraciones y accesos rápidos según rol.
- **POS / caja:** búsqueda/código de barras, carrito, precios, descuento autorizado, receta cuando aplique, medios de pago, resultado de operación y comprobante permitido.
- **Ventas:** historial, detalle de venta, pagos, documento tributario vinculado, devoluciones/correcciones y estado de conciliación.
- **Catálogo:** listado, ficha del producto/presentación, códigos, clasificación de venta, estado de validación, laboratorio/titular y relaciones con proveedores.
- **Inventario:** stock por sucursal/bodega/lote, vencimientos, movimientos, conteos, ajustes, transferencias, cuarentena y retiros.
- **Compras:** proveedores, orden de compra, recepción, diferencias, lotes capturados, facturas del proveedor y cuentas por pagar si entran en alcance.
- **Recetas/dispensación:** validación y registro de receta, líneas, cantidades, dispensación parcial cuando sea permitida, lotes y responsable; acceso restringido.
- **Caja/finanzas:** apertura, movimientos de caja, arqueo, cierre, diferencias y conciliación de medios de pago.
- **Convenios:** configuración de reglas, productos cubiertos, respuestas de elegibilidad, beneficios aplicados y liquidaciones por recuperar.
- **Reportes:** ventas, margen, inventario, vencimientos, compras, caja, beneficios y auditoría con permisos por rol.
- **Administración:** usuarios, roles, sucursales, parámetros operacionales, auditoría y estado de adaptadores externos; nunca exponer secretos.

La navegación debe ocultar las opciones no autorizadas, pero todas las operaciones deben volver a validar permisos en el backend.

---

## 3. Reglas de negocio no negociables

Estas reglas se implementan como servicios de dominio y pruebas automatizadas, no solamente como validaciones visuales.

1. **Trazabilidad:** producto vendido, presentación, lote dispensado cuando corresponda, costo/recepción, usuario, caja, pago, beneficio, receta y documento tributario deben estar relacionados.
2. **Movimientos de inventario auditables:** no modificar el stock silenciosamente. Cada recepción, venta, devolución, ajuste, transferencia, baja, cuarentena o retiro crea un movimiento con motivo, fecha, usuario y referencia.
3. **Lotes y vencimientos:** nunca seleccionar un lote vencido, retirado, dañado o en cuarentena para una venta normal. Las reglas de bloqueo deben aplicarse en backend y base de datos/servicio, no solo en el navegador.
4. **FEFO:** priorizar el lote con vencimiento más próximo que siga siendo vendible, cuando sea aplicable. La regla debe permitir excepciones autorizadas con motivo y auditoría.
5. **Concurrencia:** dos terminales no pueden vender de forma exitosa la última unidad vendible simultáneamente. Usar transacciones, bloqueo de filas/actualizaciones condicionadas y restricciones apropiadas de PostgreSQL.
6. **Dinero:** usar `Decimal` y columnas `NUMERIC`, nunca `float`. Mantener moneda explícita (CLP en los escenarios chilenos) y reglas de redondeo documentadas.
7. **Snapshot histórico:** la línea de venta conserva descripción, SKU, presentación, precio, descuentos, impuestos/configuración tributaria y costo aplicable al momento de la venta; cambios posteriores al catálogo no alteran ventas antiguas.
8. **Recetas:** condición de venta proviene de clasificación regulatoria validada, no de coincidencia de nombre. La venta/dispensación debe bloquearse si falta una validación exigida por la regla vigente.
9. **Productos controlados:** permisos separados, seguimiento de entradas/salidas/saldos/lotes y bitácora especial según requisitos confirmados por la farmacia y normativa actual.
10. **Documentos tributarios:** una respuesta incierta se consulta/reconcilia antes de volver a enviar. Nunca registrar “aceptado” sin confirmación verificable. Correcciones/anulaciones se relacionan con el documento original; no borrar una venta ya documentada.
11. **Pagos:** no marcar una venta como pagada por la mera creación de un intento. Separar estado del pago, estado de la venta y estado del documento tributario.
12. **Beneficios:** guardar regla aplicada, origen del financiamiento, importe, convenio, versión/vigencia, respuesta de validación y usuario. Diferenciar descuento financiado por la farmacia de beneficio por cobrar a un tercero.
13. **Auditoría:** cambios de precio, autorización, anulación, ajuste de stock, acceso/exportación de información sensible y acciones administrativas dejan registro no editable por usuarios operativos.
14. **Permisos:** el frontend no es un control de seguridad suficiente. Cada operación sensible se autoriza en el backend.
15. **Privacidad:** pedir y conservar solo datos necesarios para una finalidad definida; restringir recetas, RUT e historiales de dispensación por rol; no usar datos de salud para marketing por defecto.
16. **Fallos parciales:** usar estados de proceso, claves de idempotencia donde corresponda y una cola/outbox transaccional cuando haga falta garantizar entrega de eventos externos.

---

## 4. Estructura técnica sugerida del repositorio

```text
farmacia_pos/
├── README.md
├── PLAN_MAESTRO.md
├── pyproject.toml                 # Dependencias/herramientas, versiones fijadas
├── uv.lock o requirements lock    # Un lockfile único, según gestor elegido
├── .env.example                  # Solo nombres y ejemplos ficticios; sin secretos
├── .gitignore
├── Dockerfile
├── compose.yaml                  # Desarrollo: app + PostgreSQL; opcional Redis futuro
├── manage.py
├── config/
│   ├── __init__.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── development.py
│       ├── test.py
│       └── production.py
├── apps/
│   ├── core/                     # BaseModel, utilidades y errores comunes
│   ├── organizations/            # Empresa, sucursal, bodega, terminal
│   ├── accounts/                 # Usuario, roles, permisos, sesiones
│   ├── catalog/                  # Principios activos, productos, presentaciones, códigos
│   ├── suppliers/                # Proveedores, fabricantes/laboratorios, relaciones producto-proveedor
│   ├── purchasing/               # Órdenes de compra, recepción, documentos de proveedor
│   ├── inventory/                # Lotes, stock, movimientos, ajustes, transferencias, cuarentena
│   ├── pricing/                  # Listas de precio, cambios, promociones
│   ├── sales/                    # POS, ventas, líneas, devoluciones
│   ├── cash_management/          # Cajas, turnos, arqueos, cierres, egresos autorizados
│   ├── payments/                 # Intentos, pagos, devoluciones y adaptadores
│   ├── prescriptions/            # Recetas, validación, dispensaciones y restricciones
│   ├── tax_documents/            # DTE, estados, relación con ventas, adaptador tributario
│   ├── benefits/                 # Convenios, elegibilidad, topes, liquidaciones
│   ├── reporting/                # Consultas e indicadores
│   ├── audit/                    # Eventos de auditoría y acceso
│   ├── integrations/             # Contratos compartidos, outbox, cliente externo
│   └── notifications/            # Alertas internas y correo autorizado
├── templates/
│   ├── base.html
│   ├── components/
│   ├── accounts/
│   ├── catalog/
│   ├── inventory/
│   ├── purchasing/
│   ├── pos/
│   ├── prescriptions/
│   ├── reports/
│   └── administration/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── tests/
│   ├── factories/
│   ├── unit/
│   ├── integration/
│   ├── security/
│   └── acceptance/
├── docs/
│   ├── requirements/
│   ├── architecture/
│   ├── data-model/
│   ├── integrations/
│   ├── runbooks/
│   └── decisions/
├── scripts/
│   ├── seed_demo_data.py
│   └── import_validation/
└── infra/
    ├── deployment/
    ├── backup/
    └── monitoring/
```

**Nota:** esta es una estructura objetivo. No crear todos los archivos vacíos de una vez. Introducir cada aplicación cuando llegue su fase, manteniendo los límites definidos y un test mínimo por módulo.

### Convenciones internas por aplicación

```text
apps/inventory/
├── models.py
├── admin.py
├── urls.py
├── views.py
├── forms.py
├── selectors.py       # Lecturas/consultas no triviales
├── services.py        # Casos de uso y transacciones de negocio
├── policies.py        # Reglas de permiso/validación del dominio
├── validators.py
├── exceptions.py
├── migrations/
└── tests/
```

No es obligatorio usar exactamente estos nombres, pero sí separar modelos, presentación, consultas y servicios. Las vistas no deben concentrar reglas de negocio complejas.

---

## 5. Modelo de datos inicial (conceptual)

Este es un mapa lógico, no un esquema SQL definitivo. Validar campos obligatorios y periodos de conservación con el director técnico y asesores correspondientes.

### 5.1 Empresa y acceso

- `Organization`: entidad que opera la farmacia.
- `Branch`: sucursal, datos operativos, estado y zona horaria.
- `Warehouse`: bodega/ubicación de almacenamiento vinculada a sucursal.
- `Register`: caja/terminal físico.
- `User`, `Role`, `PermissionAssignment`: usuario y permisos por organización/sucursal.
- `CashShift`: turno de caja, apertura, responsable, cierre y estado.

### 5.2 Catálogo

- `ActiveIngredient`: principio activo/DCI (opcional si aún no se carga fuente válida).
- `PharmaceuticalProduct`: producto registrado/autorizado con código/registro y estado validado.
- `Presentation`: concentración, forma farmacéutica, vía, unidades por envase y unidad comercial.
- `Barcode`: uno o más códigos de identificación ligados a la presentación.
- `Laboratory`/`Manufacturer`/`RegistrationHolder`: entidades separadas cuando no coincidan.
- `ProductSupplier`: relación N:M con código de proveedor, costo, vigencia y condiciones.
- `SaleCondition`: clasificación aprobada/validada (venta directa, receta, retenida, receta cheque u otra categoría confirmada).
- `StorageRequirement`: temperatura/cadena de frío/restricciones de almacenamiento cuando aplique.

### 5.3 Compras e inventario

- `PurchaseOrder`, `PurchaseOrderLine`.
- `GoodsReceipt`, `GoodsReceiptLine` (cantidades ordenadas vs. recibidas, discrepancias).
- `Batch`/`Lot`: producto/presentación, lote, vencimiento, costo de recepción y estado.
- `StockBalance`: cantidad vendible/comprometida por sucursal, bodega, presentación y lote (si se materializa como saldo, mantenerlo consistente con el kardex).
- `InventoryMovement`: movimiento inmutable con tipo, cantidad signada, lote, origen/destino, usuario, motivo, timestamp y documento relacionado.
- `StockAdjustment`, `StockTransfer`, `Quarantine`, `Recall/MarketWithdrawal`, `PhysicalCount`.
- `SupplierInvoice` y `AccountsPayable` solo con el alcance financiero requerido.

### 5.4 POS, pagos y documentos

- `Sale`: sucursal, caja/turno, cajero, estado, moneda, totales, fecha y clave de idempotencia.
- `SaleLine`: presentación y snapshot de descripción/código/precio/impuestos/descuentos/costo utilizado.
- `SaleLotAllocation`: uno o varios lotes asignados a cada línea cuando aplique.
- `PaymentAttempt`, `Payment`: medio, referencia externa, importe, estado y marcas de tiempo; sin datos secretos de tarjeta.
- `Refund/Return`: operación vinculada a venta original, motivo, restitución de dinero y evaluación sanitaria del producto.
- `TaxDocument`: tipo, folio, monto, estado, payload/referencia segura, respuesta del proveedor/SII y documento relacionado.
- `TaxSubmissionAttempt`: intentos, respuesta, error, fecha y mecanismo de reconciliación.
- `OutboxEvent`: evento externo pendiente de envío con clave idempotente, estado y reintentos cuando sea necesario.

### 5.5 Recetas, dispensación y productos controlados

- `Prescription`: tipo, origen (electrónica/física), folio/código, estado de verificación, vencimiento/fecha cuando corresponda, referencias mínimas al paciente y prescriptor cuando sean legalmente exigibles.
- `PrescriptionLine`: producto/presentación, cantidad prescrita y campos necesarios validados.
- `Dispensation`: receta, venta, sucursal, responsable, fecha, estado.
- `DispensationLine`: cantidad autorizada/entregada, lote(s), saldo cuando la dispensación parcial esté permitida.
- Registro especial de movimientos/saldos de productos sujetos a control, con permisos y reportes que confirme el responsable sanitario.

### 5.6 Convenios y precios

- `PriceList`, `PriceListEntry`, `PriceChange`.
- `Promotion`.
- `Agreement/BenefitProgram`, `EligibilityRule`, `BenefitRule`, `CoveredProduct`, `BenefitApplication`, `Settlement/Receivable`.
- Campos de vigencia, topes, acumulación, validación, tipo de financiamiento, referencia de respuesta y auditoría.
- `CenabastProgram`/configuración de canasta/precio solo cuando el local esté adherido y la regla real esté confirmada.

### 5.7 Auditoría, notificaciones y reportes

- `AuditEvent`: actor, acción, recurso, identificador, fecha, sucursal, motivo y metadata mínima; nunca guardar contraseñas, secretos o contenido excesivo de recetas en logs.
- `Notification`: tipo, destinatario autorizado, estado y referencia al evento.
- Reportes derivan de ventas, movimientos, compras, pagos, documentos y convenios; no deben duplicar registros fuente sin reconciliación.

### Relaciones y restricciones importantes

- Cada movimiento de inventario debe referenciar su origen operacional cuando corresponda.
- Una venta confirmada contiene al menos una línea; sus totales se recalculan desde el backend.
- Un lote pertenece a un producto/presentación identificable y posee fecha de vencimiento cuando corresponda.
- Usar `PROTECT`/restricciones apropiadas para impedir que borrar un producto elimine ventas históricas; catalogar inactivación lógica.
- Importes monetarios guardados en `NUMERIC/Decimal`; fechas almacenadas en UTC y mostradas en zona horaria configurada.
- El borrado físico de ventas, pagos, movimientos y documentos operacionales queda prohibido para usuarios; corregir mediante operaciones reversibles relacionadas.

---

## 6. Flujos críticos que deben diseñarse antes del código

### 6.1 Recepción de compra

1. Crear orden con proveedor, productos/presentaciones, cantidades y costos pactados.
2. Registrar recepción real; permitir diferencias respecto de la orden.
3. Capturar lotes, vencimientos, ubicación y condición de almacenamiento; no suponer que la factura trae esos datos.
4. Separar cuarentena/no vendible de stock vendible.
5. Confirmar recepción mediante transacción y generar movimientos de inventario.
6. Registrar discrepancias de factura/orden y documentos/pagos por pagar según alcance.
7. Auditar usuario, fecha y documento.

### 6.2 Venta POS

1. Validar usuario, sucursal, caja abierta y permisos.
2. Buscar por código, SKU o texto; mostrar presentación y restricciones relevantes.
3. Verificar precio vigente, reglas de promoción y beneficio autorizado.
4. Validar condición de venta y receta cuando aplique.
5. Calcular en servidor totales, redondeos y saldo a pagar.
6. Al confirmar, bloquear/validar el stock necesario y asignar lotes vendibles por FEFO según regla.
7. Crear venta, líneas snapshot, asignación de lote, movimiento, dispensación (si aplica) y pago según estados; hacerlo dentro de transacciones controladas.
8. Ejecutar pago por el proveedor/terminal elegido; usar idempotencia y estados `pending/succeeded/failed/unknown` o equivalentes.
9. Crear/enviar documento tributario con adaptador autorizado; estados separados de la venta y del pago.
10. Si el resultado de pago o documento es desconocido, reconciliar antes de reintentar.
11. Imprimir/mostrar comprobante permitido por el modelo tributario configurado.
12. Registrar auditoría y liberar la caja a la siguiente operación.

### 6.3 Devolución

1. Buscar venta/documento original.
2. Verificar elegibilidad comercial y procedimiento aplicable.
3. Registrar devolución relacionada, motivo, líneas y cantidad.
4. Emitir la documentación tributaria de corrección que corresponda; no borrar documento original.
5. Reintegrar dinero por el método permitido.
6. Evaluar por separado el estado sanitario/comercial del medicamento; la devolución del dinero no implica que pueda volver al stock vendible.
7. Crear movimiento de inventario hacia stock vendible, cuarentena o baja según decisión autorizada.

### 6.4 Documento tributario con respuesta incierta

- Guardar identificador interno y clave idempotente antes de llamar al servicio.
- Registrar el intento y respuesta de forma segura.
- Si se corta la conexión o la respuesta es ambigua, marcar `UNKNOWN/PENDING_RECONCILIATION`.
- Consultar estado según documentación oficial/proveedor antes de un nuevo envío.
- No repetir ciegamente la emisión ni marcar aceptación sin confirmación.

### 6.5 Ajuste/transferencia de stock

- Motivo obligatorio, usuario autorizado, cantidad, lote y ubicación.
- Transferencia: salida en origen y recepción en destino relacionadas, con estado intermedio si está en tránsito.
- Conteo físico: registrar cantidad contada, diferencia y autorización; no sobreescribir saldo anterior.
- Toda diferencia queda auditable.

---

## 7. Backlog: tareas detalladas y orden de ejecución

**Prioridades:** P0 = bloquea el resto o es requisito de seguridad/consistencia; P1 = requisito operativo principal; P2 = mejora/expansión. Cada tarea debe terminar con pruebas, documentación y una evidencia de ejecución.

### Fase 0 — Descubrimiento y decisiones (antes de programar)

- [ ] **DISC-01 (P0) — Confirmar alcance del negocio.** Determinar número de sucursales/bodegas, cajas, usuarios y turnos; ventas minoristas/empresas; despacho/web si existirá. **Aceptación:** acta de decisiones firmada por dueño/responsable.
- [ ] **DISC-02 (P0) — Acordar catálogo y fuentes.** Definir origen autorizado de registro sanitario, productos, presentaciones, códigos de barras, laboratorios y proveedores. **Aceptación:** fuente y proceso de actualización documentados; sin importar datos no verificados como verdad regulatoria.
- [ ] **DISC-03 (P0) — Inventariar categorías reguladas.** Confirmar si hay recetas simples, retenidas, cheque, estupefacientes/psicotrópicos y cadena de frío. **Aceptación:** matriz de categorías revisada por director técnico.
- [ ] **DISC-04 (P0) — Levantar proceso tributario actual.** Confirmar SII, software/proveedor, modelo voucher/boleta, facturación, notas de crédito y certificación aplicable con contador. **Aceptación:** decisión por escrito y responsable de la integración.
- [ ] **DISC-05 (P0) — Definir medios de pago.** Identificar terminal/proveedor, tipos de pago, pagos mixtos, anulaciones y devoluciones. **Aceptación:** documentación técnica/contractual obtenida o pago explícitamente simulado en MVP.
- [ ] **DISC-06 (P0) — Levantar convenios.** Enumerar cada convenio, reglas, financiación, vigencia, topes y método de validación. **Aceptación:** ninguno se marca como integrable sin confirmar acceso.
- [ ] **DISC-07 (P0) — Definir privacidad y conservación.** Inventario de datos personales/sensibles, finalidades, usuarios que acceden, exportación, retención y eliminación. **Aceptación:** revisión legal/operativa registrada.
- [ ] **DISC-08 (P0) — Definir MVP y fuera de alcance.** Aprobar funcionalidades para la demo y condiciones para pasar a piloto real. **Aceptación:** alcance congelado para el primer ciclo.
- [ ] **DISC-09 (P1) — Preparar datos de prueba.** Crear ejemplos ficticios de productos, proveedores, lotes, ventas, recetas y beneficios. **Aceptación:** los datos no identifican pacientes/personas reales.

### Fase 1 — Repositorio, entorno y arquitectura

- [ ] **SETUP-01 (P0) — Crear repositorio Git.** Añadir ramas/trabajo por feature, reglas de revisión y formato de commits. **Aceptación:** repositorio limpio, `.gitignore`, licencia/privacidad decididas si aplica.
- [ ] **SETUP-02 (P0) — Fijar Python/Django/DB.** Verificar compatibilidad oficial; crear lockfile. **Aceptación:** versión reproducible registrada.
- [ ] **SETUP-03 (P0) — Configurar Django.** Settings separados para desarrollo, test y producción. **Aceptación:** `check` pasa; secretos no están en código.
- [ ] **SETUP-04 (P0) — Conectar PostgreSQL.** Usar base distinta para pruebas y desarrollo. **Aceptación:** migraciones aplican sobre PostgreSQL desde un entorno limpio.
- [ ] **SETUP-05 (P0) — Docker Compose o guía local.** Documentar arranque paso a paso y variables `.env.example`. **Aceptación:** otra persona puede instalar y levantar el proyecto siguiendo README.
- [ ] **SETUP-06 (P0) — CI inicial.** Ejecutar chequeos, formato y pruebas al hacer push/PR si la plataforma lo permite. **Aceptación:** CI falla cuando un test o lint falla.
- [ ] **SETUP-07 (P1) — Registrar decisiones arquitectónicas (ADR).** Documentar monolito modular, stack, moneda, zona horaria, modelo de errores e integraciones. **Aceptación:** decisiones clave explicadas y fechadas.

### Fase 2 — Base común, usuarios y seguridad

- [ ] **AUTH-01 (P0) — Modelo de usuario.** Configurar el usuario personalizado antes de crear dependencias fuertes del esquema. **Aceptación:** migración inicial limpia; identificador y estado adecuados.
- [ ] **AUTH-02 (P0) — Roles y permisos.** Roles iniciales: cajero, químico farmacéutico/director técnico, bodega, comprador, administrador, contador/solo lectura. **Aceptación:** pruebas positivas y negativas para cada acción crítica.
- [ ] **AUTH-03 (P0) — Separación por sucursal.** Limitar datos/acciones al ámbito asignado cuando corresponda. **Aceptación:** un usuario de una sucursal no accede sin autorización a otra.
- [ ] **AUTH-04 (P0) — Auditoría común.** Registrar actor, acción, objeto, fecha, sucursal y motivo para cambios críticos. **Aceptación:** permisos operativos no permiten alterar/borrar la auditoría.
- [ ] **AUTH-05 (P0) — Seguridad web.** CSRF, cookies seguras en producción, contraseñas, sesión, límites de acceso, configuración TLS y secretos. **Aceptación:** revisión contra checklist oficial de despliegue Django.
- [ ] **AUTH-06 (P1) — Autenticación administrativa reforzada.** MFA/2FA si es viable para cuentas privilegiadas, o control compensatorio documentado. **Aceptación:** cuentas privilegiadas protegidas.

### Fase 3 — Organización y catálogo farmacéutico

- [ ] **CAT-01 (P0) — Organización, sucursal, bodega y caja.** Crear entidades configurables. **Aceptación:** producto/stock se puede consultar en el ámbito correcto.
- [ ] **CAT-02 (P0) — Modelo de producto/presentación.** Separar producto autorizado, presentación, concentración, forma, vía y unidad comercial. **Aceptación:** un principio activo puede relacionarse con distintos productos/presentaciones sin duplicar identidad.
- [ ] **CAT-03 (P0) — Laboratorio/fabricante/titular.** Entidades separadas y relaciones explícitas. **Aceptación:** el sistema permite que sean entidades distintas.
- [ ] **CAT-04 (P0) — Códigos y búsquedas.** SKU interno, EAN/GTIN y códigos del proveedor cuando existan. **Aceptación:** búsqueda por código de barras y texto funciona; colisiones detectadas.
- [ ] **CAT-05 (P0) — Clasificación de condición de venta.** Campo con fuente/fecha de validación/estado. **Aceptación:** no se permite derivarla automáticamente del nombre del producto.
- [ ] **CAT-06 (P0) — Estado regulatorio y de catálogo.** Activo, inactivo, pendiente de verificar, bloqueado/retirado. **Aceptación:** los productos no validados no pueden ofrecerse para venta real si eso es requisito del flujo aprobado.
- [ ] **CAT-07 (P1) — Unidades y conversiones.** Declarar unidades compatibles y reglas de conversión. **Aceptación:** no se aplican conversiones implícitas incompatibles ni fraccionamiento por defecto.
- [ ] **CAT-08 (P1) — Importador de catálogo.** Validar esquema, duplicados, errores y reporte previo a guardar. **Aceptación:** importación de prueba no crea registros corruptos; reimportación es idempotente cuando corresponde.
- [ ] **CAT-09 (P1) — Actualización autorizada del catálogo regulatorio.** Confirmar con ISP la fuente y método permitidos para consultar/actualizar registros sanitarios. Registrar fecha, fuente, versión y resultado de cada importación. **Aceptación:** no se inventan APIs ni se actualizan datos regulatorios desde fuentes no autorizadas; si no hay acceso, mantener revisión/importación controlada.

### Fase 4 — Proveedores y compras

- [ ] **PUR-01 (P1) — Proveedores.** Contacto, código, condiciones, estado y documentos de referencia mínimos. **Aceptación:** permisos y validaciones correctos.
- [ ] **PUR-02 (P1) — Producto por proveedor.** Códigos, costos, mínimos, plazos y vigencia. **Aceptación:** varios proveedores pueden vender el mismo producto con condiciones distintas.
- [ ] **PUR-03 (P1) — Orden de compra.** Estados borrador/aprobada/enviada/parcial/completa/cancelada. **Aceptación:** transiciones controladas y auditadas.
- [ ] **PUR-04 (P1) — Recepción de compra.** Comparar orden y recepción; permitir diferencias y lotes múltiples. **Aceptación:** recepción incompleta o con diferencias queda registrada explícitamente.
- [ ] **PUR-05 (P1) — Documentos de proveedor/cuentas por pagar.** Alcance inicial definido con contador. **Aceptación:** factura/recepción no se confunden; vencimientos y saldos reconciliables.

### Fase 5 — Inventario, lotes y vencimientos

- [ ] **INV-01 (P0) — Lotes y saldo por ubicación.** Cantidades por lote, producto/presentación, vencimiento, bodega y estado. **Aceptación:** saldo auditable y consistente.
- [ ] **INV-02 (P0) — Kardex inmutable.** Movimientos de recepción, venta, devolución, ajuste, transferencia, baja y cuarentena. **Aceptación:** cada cambio de saldo tiene movimiento y referencia.
- [ ] **INV-03 (P0) — Stock disponible vs. comprometido.** Definir fórmula de stock vendible. **Aceptación:** una cantidad comprometida no puede volver a venderse.
- [ ] **INV-04 (P0) — Bloqueo de vencidos/retirados/cuarentena.** Aplicar en consulta y transacción final. **Aceptación:** test intenta vender lote no vendible y el backend lo rechaza.
- [ ] **INV-05 (P0) — FEFO.** Algoritmo de asignación de lotes. **Aceptación:** vende primero el lote más próximo a vencer dentro de los válidos, con excepción autorizada auditada.
- [ ] **INV-06 (P1) — Alertas configurables.** Ejemplo inicial 180/90/60/30 días, ajustable por responsable. **Aceptación:** alertas y filtros calculados correctamente.
- [ ] **INV-07 (P1) — Mínimos/máximos y reposición.** Parámetros por sucursal. **Aceptación:** reporte de productos a reponer sin ejecutar compras automáticamente.
- [ ] **INV-08 (P1) — Conteos y ajustes.** Registrar conteo, diferencia, aprobación y movimiento. **Aceptación:** no existe modificación silenciosa del saldo.
- [ ] **INV-09 (P1) — Transferencias.** Salida, tránsito, recepción y diferencias. **Aceptación:** cantidades origen/destino se reconcilian y quedan relacionadas.
- [ ] **INV-10 (P1) — Cuarentena, dañados y retiro.** Bloqueo, motivo, responsable y disposición. **Aceptación:** lote afectado no se vende y se puede localizar en todo el inventario.
- [ ] **INV-11 (P2) — Cadena de frío.** Eventos/mediciones/revisión según proceso aprobado. **Aceptación:** incidencias pueden bloquear lote y generan alerta.
- [ ] **INV-12 (P1) — Concurrencia.** Tests de dos ventas simultáneas de las últimas unidades. **Aceptación:** no hay sobreventa bajo carga concurrente básica.

### Fase 6 — Precios, descuentos y POS

- [ ] **POS-01 (P0) — Lista de precio e historial.** Precio por presentación/sucursal/vigencia y trazabilidad del cambio. **Aceptación:** cambios no reescriben ventas antiguas.
- [ ] **POS-02 (P0) — Pantalla de venta.** Búsqueda, código de barras, cantidad, quitar línea, subtotal, descuentos autorizados y total. **Aceptación:** usable con teclado/lector tipo teclado y sin depender de ratón para cada línea.
- [ ] **POS-03 (P0) — Cálculo en backend.** No confiar en total enviado por navegador. **Aceptación:** una petición manipulada no cambia el total validado.
- [ ] **POS-04 (P0) — Abrir/cerrar caja.** Fondo inicial, movimientos de caja autorizados, arqueo, diferencia y responsable. **Aceptación:** no se vende en turno cerrado; cierres son auditables.
- [ ] **POS-05 (P0) — Crear venta transaccional.** Líneas snapshot, reserva/asignación de lote y movimientos vinculados. **Aceptación:** error en una etapa no deja venta/stock en estado incoherente.
- [ ] **POS-06 (P1) — Pagos mixtos.** Efectivo, tarjeta y otros medios autorizados configurables. **Aceptación:** suma de pagos coincide con el saldo o queda saldo pendiente documentado según regla aprobada.
- [ ] **POS-07 (P1) — Anulación antes de finalizar.** Diferenciar carrito descartado de venta confirmada. **Aceptación:** no hay movimientos si nunca se confirmó; si ya existe, se usa operación compensatoria.
- [ ] **POS-08 (P1) — Devoluciones.** Vinculadas a venta original; evaluación separada de stock. **Aceptación:** retorno de dinero no garantiza reintegrar el producto a stock vendible.
- [ ] **POS-09 (P1) — Ticket interno/impresión.** Separar ticket de caja de documento tributario oficial. **Aceptación:** ninguna pantalla llama “boleta válida” a un comprobante no emitido según el modelo aprobado.

### Fase 7 — Pagos y documentación tributaria

- [ ] **PAY-01 (P0) — Contrato de pago.** Definir estados, idempotencia, reintentos, conciliación y cancelación. **Aceptación:** intentos no duplican cargos y no almacenan datos de tarjeta.
- [ ] **PAY-02 (P0) — Adaptador simulado.** Para tests, devolver aprobada/rechazada/pendiente/desconocida. **Aceptación:** el mock es inequívocamente de pruebas y nunca está activo en producción.
- [ ] **PAY-03 (P1) — Adaptador del proveedor real.** Implementar solo con contrato/documentación/credenciales autorizadas. **Aceptación:** pruebas sandbox y tratamiento de fallo/timeout completados.
- [ ] **TAX-01 (P0) — Modelo de documento tributario.** Tipo, estado, folio, importe, timestamps, respuesta y relaciones. **Aceptación:** estado del documento se separa de venta/pago.
- [ ] **TAX-02 (P0) — Máquina de estados DTE.** Pendiente, enviado, aceptado/validado, rechazado, desconocido/a reconciliar, corregido/anulado. **Aceptación:** transiciones inválidas se rechazan.
- [ ] **TAX-03 (P0) — Adaptador SII de prueba.** Respuestas simuladas en test con los mismos contratos internos que tendrá el real. **Aceptación:** mock no imita una API oficial inexistente ni envía datos fuera.
- [ ] **TAX-04 (P0) — Política de reintentos/reconciliación.** Consulta de estado antes de reenviar resultado incierto, según capacidad documentada. **Aceptación:** pruebas de timeout no crean doble documento.
- [ ] **TAX-05 (P1) — Certificación/integración real.** Solo tras validar el modelo tributario, documentación actual y proceso de certificación aplicable con SII/contador/proveedor. **Aceptación:** evidencia de ambiente de pruebas aprobado y autorización antes de producción.
- [ ] **TAX-06 (P1) — Corrección y devolución tributaria.** Nota/relación al documento original según norma aplicable. **Aceptación:** documento histórico original no se borra.
- [ ] **TAX-07 (P1) — Conciliación.** Comparar ventas, pagos, documentos y respuestas. **Aceptación:** reporte identifica diferencias sin modificar datos automáticamente.

### Fase 8 — Recetas, dispensación y control sanitario

- [ ] **RX-01 (P0) — Matriz de condición de venta.** Representar categorías y requisitos confirmados por responsable sanitario. **Aceptación:** cada regla tiene fuente/fecha/revisor.
- [ ] **RX-02 (P0) — Registro de receta.** Tipo, folio/código, origen, estado de validación y datos estrictamente requeridos. **Aceptación:** acceso por rol y auditoría.
- [ ] **RX-03 (P0) — Validación previa a la dispensación.** Determinar condiciones, vigencia, identidad/autoridad y requisitos a confirmar legalmente. **Aceptación:** no se completa la dispensación cuando falla una condición obligatoria.
- [ ] **RX-04 (P0) — Dispensación relacionada a venta/lotes.** Cantidad prescrita/entregada, responsable, hora y sucursal. **Aceptación:** traza receta → dispensación → venta → lote(s) → documento.
- [ ] **RX-05 (P1) — Dispensación parcial.** Saldo pendiente solo si normativa y tipo de receta lo permiten. **Aceptación:** no se permite por defecto; cada caso se valida por regla.
- [ ] **RX-06 (P0) — Controles especiales.** Accesos, saldos y movimientos de estupefacientes/psicotrópicos según la norma actual y proceso local. **Aceptación:** pruebas de usuario no autorizado y diferencias; validación por director técnico.
- [ ] **RX-07 (P1) — Integración SNRE.** Documentar autenticación, acreditación, endpoints, FHIR, contratos, ambientes y soporte solo cuando MINSAL lo confirme. **Aceptación:** el adaptador real requiere pruebas de certificación/acceso confirmado; si no hay acceso, el módulo registra el procedimiento manual permitido sin fingir validación en línea.
- [ ] **RX-08 (P1) — Bioequivalencia/alternativas.** Catalogar relación validada sin sustitución automática. **Aceptación:** una alternativa solo se muestra bajo criterios aprobados; la decisión profesional se respeta.

### Fase 9 — Convenios, descuentos y CENABAST

- [ ] **BEN-01 (P1) — Motor de reglas.** Elegibilidad, productos cubiertos, porcentajes/precios/copedago, vigencia, topes y acumulación. **Aceptación:** regla inválida/vencida/no elegible no aplica.
- [ ] **BEN-02 (P1) — Separar financiación.** Precio lista, promoción, descuento de farmacia y beneficio de tercero como conceptos separados. **Aceptación:** informes pueden explicar quién financió cada importe.
- [ ] **BEN-03 (P1) — Adaptador por convenio.** API/portal/manual según acuerdo concreto. **Aceptación:** no existe una supuesta API universal; el estado de validación y evidencia quedan registrados.
- [ ] **BEN-04 (P1) — Liquidación y cuentas por cobrar.** Calcular importe a recuperar, documentos y estado. **Aceptación:** conciliación por convenio y periodo.
- [ ] **BEN-05 (P1) — CENABAST.** Registrar adhesión, canasta y vigencia; aplicar condiciones solo a productos/presentaciones cubiertos según reglas reales. **Aceptación:** no se aplica precio máximo automáticamente a todos los productos del mismo principio activo.
- [ ] **BEN-06 (P0) — Privacidad en consulta por RUT.** Validar finalidad y autorización, no inferir atributos sensibles. **Aceptación:** cada flujo documenta por qué solicita el RUT y no lo usa como contraseña.

### Fase 10 — Reportes y administración

- [ ] **RPT-01 (P1) — Ventas y descuentos.** Bruto, descuentos, devoluciones y neto. **Aceptación:** definiciones documentadas y conciliables.
- [ ] **RPT-02 (P1) — Margen y costo.** Por producto/categoría/laboratorio/sucursal y periodo. **Aceptación:** diferencia claramente costo histórico y costo actual.
- [ ] **RPT-03 (P1) — Inventario.** Valor al costo, stock, vencimientos, rotación, días de inventario, quiebres y mermas. **Aceptación:** se calcula a partir de fuentes reconciliables.
- [ ] **RPT-04 (P1) — Caja/medios de pago.** Ventas por usuario/turno/medio, arqueo y diferencias. **Aceptación:** dinero recibido no se confunde con ingreso neto ni margen.
- [ ] **RPT-05 (P1) — Compras/proveedores.** Pendientes de recepción, costos comparables, cuentas por pagar. **Aceptación:** órdenes, recepciones y facturas se distinguen.
- [ ] **RPT-06 (P1) — Convenios.** Beneficios rechazados, por recuperar y liquidaciones. **Aceptación:** importes están vinculados a aplicación y regla.
- [ ] **RPT-07 (P1) — Filtros y exportación.** Exportación autorizada con auditoría. **Aceptación:** permisos limitan campos/filas y cada exportación sensible queda registrada.

### Fase 11 — Privacidad, despliegue y operación

- [ ] **OPS-01 (P0) — Configuración de producción segura.** Secretos en variables/secret manager, DEBUG apagado, hosts/orígenes configurados, TLS y cookies seguras. **Aceptación:** checklist de despliegue pasa.
- [ ] **OPS-02 (P0) — Política de datos y accesos.** Inventario de datos, finalidad, permisos, retención y eliminación. **Aceptación:** revisión de la Ley 19.628 y Ley 21.719 aplicables al lanzamiento.
- [ ] **OPS-03 (P0) — Respaldos automáticos.** Copia de DB y archivos relevantes, cifrada y separada. **Aceptación:** backup reciente verificable y procedimiento documentado.
- [ ] **OPS-04 (P0) — Prueba de restauración.** Restaurar en entorno aislado y verificar relaciones/datos. **Aceptación:** simulacro documentado, no solo existencia del archivo.
- [ ] **OPS-05 (P1) — Logs y alertas.** Errores, colas, estados desconocidos, copias de seguridad fallidas y disponibilidad. **Aceptación:** se puede diagnosticar sin exponer recetas, RUT, credenciales ni secretos.
- [ ] **OPS-06 (P1) — Plan de incidentes.** Indisponibilidad de Internet/SII/SNRE/pagos, errores de conciliación, pérdida de equipo y acceso indebido. **Aceptación:** responsable y pasos manuales autorizados documentados.
- [ ] **OPS-07 (P1) — Despliegue de staging.** Entorno similar a producción con datos ficticios y configuración aislada. **Aceptación:** ninguna credencial ni dato real de producción está en staging.
- [ ] **OPS-08 (P0) — Validación operativa formal.** Pruebas con cajero, responsable de bodega, director técnico y contador según sus áreas. **Aceptación:** firmas/aprobaciones o una lista explícita de defectos pendientes; sin aprobación, no se habilita producción.

---

## 8. Estrategia de pruebas y criterios de aceptación globales

### Tipos de prueba

1. **Unitarias:** cálculos, reglas de precio, FEFO, permisos, condiciones de venta, estados y redondeo.
2. **Integración:** ORM + PostgreSQL, servicios, transacciones, locks, outbox y adaptadores simulados.
3. **Seguridad:** usuarios con permisos insuficientes, acceso cruzado por sucursal, CSRF, exportaciones, secretos, registros de auditoría.
4. **Aceptación funcional:** flujos completos de compra, recepción, venta, pago, documento, receta, devolución y cierre de caja.
5. **Resiliencia:** timeout, respuesta desconocida, caída externa, retry, duplicado, restore de backup y operaciones simultáneas.
6. **Usabilidad de caja:** teclado/lector de código de barras, tiempos de respuesta básicos, mensaje claro al cajero y recuperación de errores.

### Casos mínimos derivados del PDF

- Venta con varios productos y distintos medios de pago.
- Documento tributario sin respuesta inmediata del servicio externo.
- Corrección/anulación de boleta.
- Producto con múltiples proveedores y costos.
- Dos lotes con fechas de vencimiento distintas; FEFO correcto.
- Intento de venta de medicamento sujeto a receta sin receta válida.
- Dispensación parcial solo cuando la regla lo autorice.
- Producto controlado con autorización inválida o usuario no autorizado.
- Beneficio aplicado a paciente/persona no elegible.
- Dos ventas simultáneas de las últimas unidades.
- Devolución de producto no apto para reingresar a stock vendible.
- Usuario sin permisos intenta cambiar precios, borrar movimientos o acceder a recetas.

### Definición de Hecho (DoD) de cada tarea

Una tarea solo se considera terminada si:

- [ ] cumple su criterio de aceptación;
- [ ] incluye pruebas automatizadas relevantes (positivas, negativas y límites);
- [ ] las migraciones se aplican sobre una DB vacía y sobre la DB de desarrollo;
- [ ] no rompe pruebas ni lint;
- [ ] los permisos de backend están comprobados;
- [ ] se registraron decisiones/campos sensibles en documentación;
- [ ] interfaz muestra estados y errores útiles sin filtrar información sensible;
- [ ] se actualizó `README` o guía operativa si cambió la forma de ejecutar/configurar;
- [ ] se añadió auditoría para operaciones sensibles;
- [ ] el cambio no activa integraciones ficticias en producción.

---

## 9. Instrucciones de trabajo para el otro agente de IA

Copia este bloque como instrucciones permanentes del agente que programará el proyecto:

> Trabaja como ingeniero de software senior responsable de un sistema POS y de administración farmacéutica para Chile. Sigue el archivo `PLAN_MAESTRO.md` y el documento base `analisis_integral_farmacia_chile.pdf`.
>
> **No generes toda la aplicación de una sola vez.** Implementa una tarea del backlog por vez, en orden de dependencias. Antes de modificar código, identifica la tarea (ID), los módulos/archivos afectados, reglas del negocio y pruebas que agregarás. Después implementa el cambio, ejecuta las pruebas/lint/chequeos, informa la salida real de los comandos y actualiza el checklist. No digas que algo funciona si no se ejecutó o no se comprobó.
>
> Mantén la arquitectura como monolito modular Django + PostgreSQL. Las vistas solo coordinan entrada/salida; las reglas se ubican en servicios de dominio. Dinero con Decimal/NUMERIC. Inventario con movimientos auditables, transacciones y protección contra venta concurrente de la última unidad. Las ventas históricas conservan snapshots. No borrar movimientos, ventas ni documentos operacionales para corregirlos: usar operaciones compensatorias relacionadas.
>
> Nunca inventes APIs, endpoints, contratos, credenciales ni certificaciones de SII, MINSAL/SNRE, ISP, CENABAST, operadores de pago o convenios. Si falta documentación/acceso, crea únicamente una interfaz de adaptador y un mock claramente limitado al entorno de pruebas; documenta el bloqueo y sigue con módulos que no dependan de él. Ningún mock puede activarse en producción.
>
> No guardes número completo de tarjeta, CVV, contraseñas, claves de API, secretos ni datos sensibles innecesarios en logs. No afirmes cumplimiento legal/sanitario. Marca los puntos que requieren revisión del contador, director técnico, asesor legal u organismo oficial.
>
> No añadas dependencias, apps ni abstracciones sin necesidad concreta. Mantén `README`, `.env.example`, tests y documentación actualizados. No cambies tecnologías fundamentales o modelo de datos sin explicar impacto y registrar la decisión.
>
> Al finalizar cada tarea entrega: (1) resumen; (2) archivos creados/modificados; (3) migraciones; (4) comandos ejecutados y resultados reales; (5) riesgos/decisiones pendientes; (6) tarea siguiente recomendada. Si falla algo, informa el fallo con claridad y no continúes como si hubiera pasado.

### Formato obligatorio de respuesta del agente por tarea

```text
Tarea: INV-04 — Bloqueo de lotes no vendibles
Estado: HECHA / PARCIAL / BLOQUEADA
Archivos modificados:
Migraciones:
Reglas implementadas:
Pruebas añadidas:
Comandos ejecutados y resultado real:
Criterios de aceptación (cumplidos/no cumplidos):
Riesgos y decisiones pendientes:
Siguiente tarea sugerida:
```

---

## 10. Datos y variables de configuración

Crear `.env.example` sin secretos reales. Variables de ejemplo:

```dotenv
DJANGO_SETTINGS_MODULE=config.settings.development
SECRET_KEY=replace-me-for-local-development-only
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://farmacia_app:local-only-password@localhost:5432/farmacia_dev
TIME_ZONE=America/Santiago
CURRENCY_CODE=CLP
PAYMENT_MODE=mock
TAX_DOCUMENT_MODE=mock
PRESCRIPTION_INTEGRATION_MODE=manual_or_mock
```

En producción usar secret manager/variables seguras; no copiar contraseñas de ejemplo. Las flags `mock` deben rechazarse explícitamente si `DEBUG=false` o configuración de producción. Los modos manuales deben corresponder a un procedimiento aprobado, no a una evasión de requisitos legales.

---

## 11. Orden recomendado de entregas y puertas de control

### Entrega A — Fundaciones

DISC-01 a DISC-09, SETUP-01 a SETUP-07, AUTH-01 a AUTH-05. No avanzar a operaciones reales hasta tener roles, seguridad, PostgreSQL y CI.

### Entrega B — Catálogo y stock fiable

CAT-01 a CAT-08, PUR-01 a PUR-04 e INV-01 a INV-12 (ordenando dependencias). Puerta: ninguna operación puede modificar stock sin movimiento; lotes y estados bloquean correctamente; se supera test concurrente de última unidad.

### Entrega C — POS en modo de prueba

POS-01 a POS-09, PAY-01 y PAY-02, TAX-01 a TAX-04. Puerta: flujos de venta/pago/documento simulado conciliables, idempotentes y sin duplicados; no se conecta a producción.

### Entrega D — Reglas farmacéuticas y convenios

RX-01 a RX-06 y BEN-01 a BEN-06. Puerta: revisión del director técnico/responsable sanitario; requisitos no confirmados quedan inhabilitados en modo real.

### Entrega E — Integraciones autorizadas

PAY-03, TAX-05 a TAX-07, RX-07 y BEN-03/BEN-05 específicos. Puerta: contratos, credenciales, ambiente de pruebas y autorizaciones verificadas.

### Entrega F — Operación y producción

RPT-01 a RPT-07, OPS-01 a OPS-08. Puerta final: seguridad, backup/restore, entrenamiento, aprobación operativa, pruebas de aceptación y plan de contingencia completados.

No asignar fechas calendario hasta conocer disponibilidad del dueño, experiencia del programador, datos de catálogo, equipos y accesos de terceros. Estimar el esfuerzo por tarea después de la Fase 0.

---

## 12. Decisiones que deben quedar documentadas antes de producción

- [ ] Entidad legal, RUT de la empresa y sucursales a configurar.
- [ ] Quién es responsable técnico y quién valida las condiciones de dispensación.
- [ ] Qué datos maestros se importan y quién mantiene su exactitud.
- [ ] Categorías de medicamentos y procesos especiales aplicables.
- [ ] Método autorizado para emisión de DTE y modelo voucher/boleta.
- [ ] Operador de pago, terminales y contrato/API vigente.
- [ ] Convenios vigentes y proceso de elegibilidad/liquidación por cada uno.
- [ ] Estado real de adhesión a CENABAST y canasta aplicable, si corresponde.
- [ ] Acceso/acreditación/documentación vigente para SNRE si se integrará.
- [ ] Fuente autorizada para consultar/actualizar registros sanitarios del ISP.
- [ ] Base legal/finalidades/periodos de conservación de datos personales y de salud.
- [ ] Plan de contingencia de Internet, pagos, SII, SNRE y hardware.
- [ ] Proveedor de hosting, responsable de respaldos y responsable de incidentes.
- [ ] Hardware: lectores de código, impresora, cajón, terminal de pago y red.
- [ ] Procedimiento de migración desde sistema anterior si existe.

---

## 13. Fuentes que deben mantenerse verificadas

### Fuente principal del alcance

- Documento proporcionado por el usuario: *Análisis integral — Sistema POS y administración para una farmacia en Chile*, 24-10-2026, especialmente las secciones 1–15.

### Fuentes oficiales y técnicas consultadas para este plan (revisar de nuevo al desplegar)

- Decreto Supremo 466, Reglamento de Farmacias — Biblioteca del Congreso Nacional de Chile: https://www.bcn.cl/leychile/Navegar?idNorma=13613
- Ley 21.719 de protección y tratamiento de datos personales — Biblioteca del Congreso Nacional: https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=1209272
- Instructivo técnico de Boleta Electrónica — SII: https://www.sii.cl/servicios_online/3532-instructivo_tecnico_be-3811.html
- Consulta pública del Reglamento de Receta Electrónica — MINSAL, marzo de 2025 (es una propuesta/documento de consulta; no asumir que cada detalle sea el reglamento final): https://www.minsal.cl/wp-content/uploads/2025/12/CONSULTA-PUBLICA-REGLAMENTO-DE-RECETA-ELECTRONICA-.pdf
- Versiones y soporte de Django: https://www.djangoproject.com/download/
- Matriz de versiones de Python compatibles con Django: https://docs.djangoproject.com/en/6.1/faq/install/
- Política de versiones soportadas de PostgreSQL: https://www.postgresql.org/support/versioning/

**Fecha de revisión web para la redacción de este plan:** 24-10-2026. El estado técnico/regulatorio puede cambiar. Confirmar la versión vigente y condiciones específicas con fuente oficial antes de producción.

---

## 14. Criterio final de éxito

El sistema solo se considera listo para piloto cuando puede responder, de forma comprobable y auditable:

- qué se vendió y en qué presentación;
- de qué lote(s) salió y qué vencimiento tenían;
- cuándo y a qué costo se recibió ese lote;
- qué condición de dispensación se aplicó y quién la validó;
- qué receta/dispensación se relaciona, cuando corresponde;
- qué descuento/beneficio se aplicó, bajo qué regla y quién lo financió;
- cómo se cobró y qué estado confirmó el proveedor de pago;
- qué documento tributario respalda la operación y cuál es su estado confirmado;
- qué cambios o incidencias ocurrieron y quién los realizó;
- cómo se restaura el sistema y se recupera la operación tras una falla.

La producción requiere que los procesos regulatorios, tributarios, de privacidad y de pagos se hayan validado con los responsables correspondientes. El código por sí solo no reemplaza dichas validaciones.
