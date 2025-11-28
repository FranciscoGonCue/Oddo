# 🏗️ Arquitectura del Sistema - Taberna de Moe

## 📁 Estructura Modular

El proyecto está organizado en **apps independientes** siguiendo las mejores prácticas de Django:

```
Oddo/
├── oddo_project/          # Configuración del proyecto
│   ├── settings.py        # Configuración general
│   ├── urls.py           # URLs principales
│   └── wsgi.py
│
├── core/                  # 📦 MÓDULO CORE (Base)
│   ├── models.py         # Partner, Product
│   ├── serializers.py    # PartnerSerializer, ProductSerializer
│   ├── views.py          # PartnerViewSet, ProductViewSet
│   ├── urls.py           # /api/partners/, /api/products/
│   └── admin.py          # Admin para Partners y Products
│
├── purchases/             # 🛒 MÓDULO COMPRAS
│   ├── models.py         # PurchaseOrder, PurchaseOrderLine
│   ├── serializers.py    # PurchaseOrderSerializer
│   ├── views.py          # PurchaseOrderViewSet
│   ├── urls.py           # /api/purchase-orders/
│   └── admin.py          # Admin para órdenes de compra
│
├── inventory/             # 🏭 MÓDULO INVENTARIO
│   ├── models.py         # Warehouse, StockQuant
│   ├── serializers.py    # WarehouseSerializer, StockQuantSerializer
│   ├── views.py          # WarehouseViewSet, StockQuantViewSet
│   ├── urls.py           # /api/warehouses/, /api/stock-quants/
│   └── admin.py          # Admin para almacenes y stock
│
├── pos/                   # 🖥️ MÓDULO PUNTO DE VENTA
│   ├── models.py         # PosOrder, PosOrderLine
│   ├── serializers.py    # PosOrderSerializer, PosOrderLineSerializer
│   ├── views.py          # PosOrderViewSet, PosOrderLineViewSet
│   ├── urls.py           # /api/pos-orders/
│   └── admin.py          # Admin para tickets de venta
│
├── invoicing/             # 📄 MÓDULO FACTURACIÓN
│   ├── models.py         # Invoice, Payment
│   ├── serializers.py    # InvoiceSerializer, PaymentSerializer
│   ├── views.py          # InvoiceViewSet, PaymentViewSet
│   ├── urls.py           # /api/invoices/, /api/payments/
│   └── admin.py          # Admin para facturas y pagos
│
├── hr/                    # 👷 MÓDULO EMPLEADOS
│   ├── models.py         # Employee
│   ├── serializers.py    # EmployeeSerializer
│   ├── views.py          # EmployeeViewSet
│   ├── urls.py           # /api/employees/
│   └── admin.py          # Admin para empleados
│
├── api/                   # (VACÍA - mantiene estructura legacy)
│   ├── models.py         # Comentarios explicativos
│   ├── serializers.py    # Comentarios explicativos
│   ├── views.py          # Comentarios explicativos
│   ├── urls.py           # URLs vacías
│   └── admin.py          # Comentarios explicativos
│
├── scripts/
│   └── demo_taberna_moe.py  # Script de demostración
│
├── db.sqlite3            # Base de datos
├── manage.py
└── README.md
```

## 🔗 Relaciones Entre Módulos

### Dependencias entre apps:

```
core (base)
  ↓
  ├─→ purchases (depende de Partner, Product)
  ├─→ inventory (depende de Product)
  ├─→ pos (depende de Partner, Product, Warehouse)
  └─→ invoicing (depende de Partner)

inventory
  ↓
  └─→ pos (depende de Warehouse, StockQuant)

invoicing
  ↓
  └─→ pos (crea facturas automáticamente)
```

## 📊 Modelos por App

### 📦 **core**
- **Partner**: Clientes, proveedores y socios
- **Product**: Productos (bebidas y comida)

### 🛒 **purchases**
- **PurchaseOrder**: Cabecera del pedido de compra
- **PurchaseOrderLine**: Líneas del pedido

### 🏭 **inventory**
- **Warehouse**: Almacenes físicos
- **StockQuant**: Stock real por producto y ubicación

### 🖥️ **pos**
- **PosOrder**: Tickets de venta
- **PosOrderLine**: Líneas del ticket

### 📄 **invoicing**
- **Invoice**: Facturas
- **Payment**: Pagos registrados

### 👷 **hr**
- **Employee**: Empleados

## 🔄 Lógica de Negocio Automática

### 1. **Fiado → Factura (pos → invoicing)**
Cuando un `PosOrder` cambia a estado `'debt'`:
1. Se crea automáticamente una `Invoice` con estado `'open'`
2. Se actualiza el `debt_balance` del `Partner`
3. Se registra el origen de la factura como referencia al ticket

### 2. **Venta → Stock (pos → inventory)**
Cuando se crea un `PosOrderLine`:
1. Se calcula automáticamente el `price_subtotal`
2. Se reduce el `StockQuant` correspondiente
3. Si no existe stock, se crea con cantidad negativa

### 3. **Pago → Deuda (invoicing → core)**
Cuando se registra un `Payment`:
1. Se reduce el `debt_balance` del `Partner`
2. Se verifica si la factura está totalmente pagada
3. Si está pagada, se cambia el estado de la `Invoice` a `'paid'`

## 🎯 Ventajas de Esta Arquitectura

### ✅ **Modularidad**
- Cada app es independiente y reutilizable
- Fácil de mantener y extender
- Responsabilidades claras y separadas

### ✅ **Escalabilidad**
- Se pueden agregar nuevas apps sin afectar las existentes
- Fácil migración a microservicios si es necesario
- Código organizado y limpio

### ✅ **Mantenibilidad**
- Cada módulo tiene su propia lógica
- Fácil localización de bugs
- Código más legible y comprensible

### ✅ **Reutilización**
- Los modelos base (core) son reutilizables
- Las apps pueden usarse en otros proyectos
- DRY (Don't Repeat Yourself)

## 🚀 Cómo Agregar un Nuevo Módulo

1. **Crear la app:**
   ```bash
   python manage.py startapp nombre_modulo
   ```

2. **Definir modelos** en `nombre_modulo/models.py`

3. **Crear serializers** en `nombre_modulo/serializers.py`

4. **Crear views** en `nombre_modulo/views.py`

5. **Definir URLs** en `nombre_modulo/urls.py`

6. **Configurar admin** en `nombre_modulo/admin.py`

7. **Registrar la app** en `settings.py`:
   ```python
   INSTALLED_APPS = [
       ...
       'nombre_modulo',
   ]
   ```

8. **Incluir URLs** en `oddo_project/urls.py`:
   ```python
   urlpatterns = [
       ...
       path('api/', include('nombre_modulo.urls')),
   ]
   ```

9. **Crear migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 📝 Notas Importantes

- La app `api` se mantiene **vacía** pero registrada en `INSTALLED_APPS` para mantener compatibilidad con migraciones antiguas
- Todas las migraciones anteriores de `api` se conservan en `api/migrations/`
- Los nuevos modelos están en sus apps específicas y tienen sus propias migraciones
- El script de demo (`scripts/demo_taberna_moe.py`) importa desde las nuevas apps modulares

## 🔒 Buenas Prácticas Implementadas

1. **Separation of Concerns**: Cada app tiene una responsabilidad específica
2. **DRY**: No hay duplicación de código
3. **Single Responsibility**: Cada módulo hace una cosa y la hace bien
4. **Dependency Injection**: Las apps dependen de interfaces, no de implementaciones
5. **Clean Architecture**: Lógica de negocio separada de la capa de presentación
