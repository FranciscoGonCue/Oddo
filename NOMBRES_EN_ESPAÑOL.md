# 🇪🇸 API Taberna de Moe - Nombres en Español

## ✅ Cambios Realizados

Todos los modelos, campos, serializers, views, admin y URLs ahora están en español.

---

## 📦 CORE Module

### Modelos
- **Partner** → **Socio**
  - `name` → `nombre`
  - `is_supplier` → `es_proveedor`
  - `debt_balance` → `saldo_deuda`
  - `created_at` → `fecha_creacion`

- **Product** → **Producto**
  - `name` → `nombre`
  - `sales_price` → `precio_venta`
  - `created_at` → `fecha_creacion`

### URLs
- `/api/partners/` → `/api/socios/`
- `/api/products/` → `/api/productos/`

### Acciones
- `/socios/suppliers/` → `/socios/proveedores/`
- `/socios/customers/` → `/socios/clientes/`
- `/socios/<id>/debt_history/` → `/socios/<id>/historial_deudas/`

---

## 🛒 PURCHASES Module

### Modelos
- **PurchaseOrder** → **OrdenCompra**
  - `supplier` → `proveedor`
  - `date_order` → `fecha_orden`
  - `state` → `estado`
    - `'draft'` → `'borrador'`
    - `'confirmed'` → `'confirmado'`

- **PurchaseOrderLine** → **LineaOrdenCompra**
  - `purchase_order` → `orden_compra`
  - `product` → `producto`
  - `quantity` → `cantidad`

### URLs
- `/api/purchase-orders/` → `/api/ordenes-compra/`
- `/api/purchase-order-lines/` → `/api/lineas-orden-compra/`

### Acciones
- `/ordenes-compra/<id>/confirm/` → `/ordenes-compra/<id>/confirmar/`

---

## 🏭 INVENTORY Module

### Modelos
- **Warehouse** → **Almacen**
  - `name` → `nombre`
  - `created_at` → `fecha_creacion`

- **StockQuant** → **CantidadStock**
  - `product` → `producto`
  - `location` → `ubicacion`
  - `quantity` → `cantidad`
  - `updated_at` → `fecha_actualizacion`

### URLs
- `/api/warehouses/` → `/api/almacenes/`
- `/api/stock-quants/` → `/api/cantidades-stock/`

### Acciones
- `/almacenes/<id>/inventory/` → `/almacenes/<id>/inventario/`

---

## 🖥️ POS Module

### Modelos
- **PosOrder** → **OrdenPOS**
  - `session_id` → `id_sesion`
  - `customer` → `cliente`
  - `date` → `fecha`
  - `state` → `estado`
    - `'draft'` → `'borrador'`
    - `'paid'` → `'pagado'`
    - `'debt'` → `'fiado'`
  - `warehouse` → `almacen`
  - `get_total()` → `obtener_total()`

- **PosOrderLine** → **LineaOrdenPOS**
  - `pos_order` → `orden_pos`
  - `product` → `producto`
  - `qty` → `cantidad`
  - `price_subtotal` → `precio_subtotal`

### URLs
- `/api/pos-orders/` → `/api/ordenes-pos/`
- `/api/pos-order-lines/` → `/api/lineas-orden-pos/`

### Acciones
- `/ordenes-pos/<id>/mark_paid/` → `/ordenes-pos/<id>/marcar_pagado/`
- `/ordenes-pos/<id>/mark_debt/` → `/ordenes-pos/<id>/marcar_fiado/`

---

## 📄 INVOICING Module

### Modelos
- **Invoice** → **Factura**
  - `origin` → `origen`
  - `partner` → `socio`
  - `amount_total` → `monto_total`
  - `state` → `estado`
    - `'open'` → `'abierto'`
    - `'paid'` → `'pagado'`
  - `due_date` → `fecha_vencimiento`
  - `created_at` → `fecha_creacion`

- **Payment** → **Pago**
  - `invoice` → `factura`
  - `amount` → `monto`
  - `method` → `metodo`
    - `'cash'` → `'efectivo'`
    - `'check'` → `'cheque'`
    - `'kind'` → `'especie'`
  - `date` → `fecha`

### URLs
- `/api/invoices/` → `/api/facturas/`
- `/api/payments/` → `/api/pagos/`

### Acciones
- `/facturas/open_invoices/` → `/facturas/facturas_abiertas/`

---

## 👷 HR Module

### Modelos
- **Employee** → **Empleado**
  - `name` → `nombre`
  - `job_title` → `puesto`
  - `created_at` → `fecha_creacion`

### URLs
- `/api/employees/` → `/api/empleados/`

---

## 🔄 Serializers

Todos los serializers fueron actualizados:
- `PartnerSerializer` → `SocioSerializer`
- `ProductSerializer` → `ProductoSerializer`
- `PurchaseOrderSerializer` → `OrdenCompraSerializer`
- `WarehouseSerializer` → `AlmacenSerializer`
- `StockQuantSerializer` → `CantidadStockSerializer`
- `PosOrderSerializer` → `OrdenPOSSerializer`
- `InvoiceSerializer` → `FacturaSerializer`
- `PaymentSerializer` → `PagoSerializer`
- `EmployeeSerializer` → `EmpleadoSerializer`

---

## 📊 ViewSets

Todos los ViewSets fueron actualizados:
- `PartnerViewSet` → `SocioViewSet`
- `ProductViewSet` → `ProductoViewSet`
- `PurchaseOrderViewSet` → `OrdenCompraViewSet`
- `WarehouseViewSet` → `AlmacenViewSet`
- `StockQuantViewSet` → `CantidadStockViewSet`
- `PosOrderViewSet` → `OrdenPOSViewSet`
- `InvoiceViewSet` → `FacturaViewSet`
- `PaymentViewSet` → `PagoViewSet`
- `EmployeeViewSet` → `EmpleadoViewSet`

---

## 🎯 Admin

Todos los modelos admin fueron actualizados con nombres en español:
- Los `list_display`, `search_fields` y `list_filter` ahora usan nombres de campos en español
- Los métodos personalizados como `get_total()` → `obtener_total()`

---

## 🚀 Endpoints Principales

### CORE
```
GET    /api/socios/                    # Listar socios
POST   /api/socios/                    # Crear socio
GET    /api/socios/<id>/               # Ver socio
GET    /api/socios/proveedores/        # Listar proveedores
GET    /api/socios/clientes/           # Listar clientes
GET    /api/socios/<id>/historial_deudas/  # Historial de deudas

GET    /api/productos/                 # Listar productos
POST   /api/productos/                 # Crear producto
GET    /api/productos/<id>/            # Ver producto
GET    /api/productos/<id>/stock/      # Ver stock del producto
```

### COMPRAS
```
GET    /api/ordenes-compra/            # Listar órdenes de compra
POST   /api/ordenes-compra/            # Crear orden de compra
GET    /api/ordenes-compra/<id>/       # Ver orden
POST   /api/ordenes-compra/<id>/confirmar/  # Confirmar orden
```

### INVENTARIO
```
GET    /api/almacenes/                 # Listar almacenes
POST   /api/almacenes/                 # Crear almacén
GET    /api/almacenes/<id>/inventario/ # Ver inventario del almacén

GET    /api/cantidades-stock/          # Listar cantidades de stock
POST   /api/cantidades-stock/          # Crear/actualizar stock
```

### POS
```
GET    /api/ordenes-pos/               # Listar tickets
POST   /api/ordenes-pos/               # Crear ticket
GET    /api/ordenes-pos/<id>/          # Ver ticket
POST   /api/ordenes-pos/<id>/marcar_pagado/   # Marcar como pagado
POST   /api/ordenes-pos/<id>/marcar_fiado/    # Marcar como fiado
```

### FACTURACIÓN
```
GET    /api/facturas/                  # Listar facturas
POST   /api/facturas/                  # Crear factura
GET    /api/facturas/facturas_abiertas/  # Facturas pendientes

GET    /api/pagos/                     # Listar pagos
POST   /api/pagos/                     # Registrar pago
```

### EMPLEADOS
```
GET    /api/empleados/                 # Listar empleados
POST   /api/empleados/                 # Crear empleado
GET    /api/empleados/<id>/            # Ver empleado
```

---

## 📝 Notas Importantes

1. **Base de datos recreada**: Se eliminó la base de datos anterior y se crearon nuevas migraciones con los nombres en español.

2. **Compatibilidad**: Los antiguos nombres en inglés ya NO funcionan. Toda la API ahora está completamente en español.

3. **Configuración regional**:
   - `LANGUAGE_CODE = 'es-es'`
   - `TIME_ZONE = 'Europe/Madrid'`
   - Formatos de fecha personalizados en español

4. **Superusuario**: 
   - Usuario: `admin`
   - Contraseña: `admin123`

5. **Acceso**:
   - API: http://127.0.0.1:8000/api/
   - Admin: http://127.0.0.1:8000/admin/

---

## ✨ Ejemplo de Uso

```python
from core.models import Socio, Producto
from inventory.models import Almacen, CantidadStock
from pos.models import OrdenPOS, LineaOrdenPOS

# Crear socio
homer = Socio.objects.create(
    nombre='Homer Simpson',
    es_proveedor=False
)

# Crear producto
cerveza = Producto.objects.create(
    nombre='Cerveza Duff',
    precio_venta=5.00
)

# Crear almacén
barra = Almacen.objects.create(nombre='Barra Principal')

# Agregar stock
stock = CantidadStock.objects.create(
    producto=cerveza,
    ubicacion=barra,
    cantidad=100
)

# Crear ticket
ticket = OrdenPOS.objects.create(
    cliente=homer,
    almacen=barra,
    estado='borrador'
)

# Agregar línea al ticket
linea = LineaOrdenPOS.objects.create(
    orden_pos=ticket,
    producto=cerveza,
    cantidad=3
)

# Marcar como pagado
ticket.estado = 'pagado'
ticket.save()
```

---

✅ **Todo está en español y funcionando correctamente**
