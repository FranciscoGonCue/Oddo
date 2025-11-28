# 🍺 Taberna de Moe - Sistema de Gestión API

_API completa con Django + Django REST Framework para la gestión integral de una taberna._

## 📁 Estructura Modular del Proyecto

El proyecto está organizado en apps independientes para facilitar el mantenimiento:

```
Oddo/
├── core/           # 📦 Partners y Products (Base)
├── purchases/      # 🛒 Órdenes de compra
├── inventory/      # 🏭 Almacenes y stock
├── pos/            # 🖥️ Punto de venta
├── invoicing/      # 📄 Facturación y pagos
├── hr/             # 👷 Empleados
└── api/            # (Vacía - legacy)
```

## 🌳 Estructura de Datos

Este sistema implementa 6 módulos funcionales:

### 📦 1. CORE (Base)
- **Partner**: Socios, clientes y proveedores (¿Es Duff? True/False)
- **Product**: Bebidas y comida del establecimiento

### 🛒 2. COMPRAS (Purchase)
- **PurchaseOrder**: Cabecera del pedido de compra
- **PurchaseOrderLine**: Detalle del pedido (productos y cantidades)

### 🏭 3. INVENTARIO (Inventory)
- **Warehouse**: Lugares físicos (Barra, Trastienda)
- **StockQuant**: Stock real en mano por ubicación

### 🖥️ 4. PUNTO DE VENTA (POS)
- **PosOrder**: Tickets de venta
- **PosOrderLine**: Líneas del ticket

### 📄 5. FACTURACIÓN (Invoicing)
- **Invoice**: La cuenta formal
- **Payment**: Registro de pagos

### 👷 6. EMPLEADOS (HR)
- **Employee**: Personal de la taberna

## Requisitos

- Python 3.8+
- pip

## Instalación y ejecución

1. **Clonar o copiar archivos** en un directorio limpio.

2. **Configurar entorno Python:**
```bash
python -m venv .venv
source .venv/bin/activate  # En macOS/Linux
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Crear base de datos:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario (opcional, para acceder al admin):**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor:**
```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000/**

Panel de administración: **http://127.0.0.1:8000/admin/**

## 📡 Endpoints API

### 📦 CORE (Base)

#### Partners
- `GET/POST /api/partners/` - Listar/crear partners
- `GET/PUT/PATCH/DELETE /api/partners/{id}/` - Operaciones con partner específico
- `GET /api/partners/suppliers/` - Listar solo proveedores
- `GET /api/partners/customers/` - Listar solo clientes
- `GET /api/partners/{id}/debt_history/` - Ver historial de deudas

#### Products
- `GET/POST /api/products/` - Listar/crear productos
- `GET/PUT/PATCH/DELETE /api/products/{id}/` - Operaciones con producto específico
- `GET /api/products/{id}/stock/` - Ver stock del producto en todos los almacenes

### 🛒 COMPRAS (Purchase)

#### Purchase Orders
- `GET/POST /api/purchase-orders/` - Listar/crear órdenes de compra
- `GET/PUT/PATCH/DELETE /api/purchase-orders/{id}/` - Operaciones con orden específica
- `POST /api/purchase-orders/{id}/confirm/` - Confirmar orden de compra

#### Purchase Order Lines
- `GET/POST /api/purchase-order-lines/` - Listar/crear líneas de pedido
- `GET/PUT/PATCH/DELETE /api/purchase-order-lines/{id}/` - Operaciones con línea específica

### 🏭 INVENTARIO (Inventory)

#### Warehouses
- `GET/POST /api/warehouses/` - Listar/crear almacenes
- `GET/PUT/PATCH/DELETE /api/warehouses/{id}/` - Operaciones con almacén específico
- `GET /api/warehouses/{id}/inventory/` - Ver inventario completo del almacén

#### Stock Quants
- `GET/POST /api/stock-quants/` - Listar/crear stock
- `GET/PUT/PATCH/DELETE /api/stock-quants/{id}/` - Operaciones con stock específico

### 🖥️ POS (Punto de Venta)

#### POS Orders
- `GET/POST /api/pos-orders/` - Listar/crear tickets
- `GET/PUT/PATCH/DELETE /api/pos-orders/{id}/` - Operaciones con ticket específico
- `POST /api/pos-orders/{id}/mark_paid/` - Marcar ticket como pagado
- `POST /api/pos-orders/{id}/mark_debt/` - Marcar como fiado (genera factura automática)

#### POS Order Lines
- `GET/POST /api/pos-order-lines/` - Listar/crear líneas de ticket
- `GET/PUT/PATCH/DELETE /api/pos-order-lines/{id}/` - Operaciones con línea específica

### 📄 FACTURACIÓN (Invoicing)

#### Invoices
- `GET/POST /api/invoices/` - Listar/crear facturas
- `GET/PUT/PATCH/DELETE /api/invoices/{id}/` - Operaciones con factura específica
- `GET /api/invoices/open_invoices/` - Listar facturas pendientes de pago

#### Payments
- `GET/POST /api/payments/` - Listar/crear pagos
- `GET/PUT/PATCH/DELETE /api/payments/{id}/` - Operaciones con pago específico

### 👷 EMPLEADOS (HR)

#### Employees
- `GET/POST /api/employees/` - Listar/crear empleados
- `GET/PUT/PATCH/DELETE /api/employees/{id}/` - Operaciones con empleado específico

### 📝 Legacy (Compatibilidad)
- `GET/POST /api/items/` - Listar/crear items
- `GET/PUT/PATCH/DELETE /api/items/{id}/` - Operaciones con item específico
- `GET/POST /api/facturas/` - Listar/crear facturas  
- `GET/PUT/PATCH/DELETE /api/facturas/{id}/` - Operaciones con factura específica

## 🔄 Lógica Automática del Sistema

### 🎯 Fiado (Deuda)
Cuando un `PosOrder` se guarda con estado "Fiado/Deuda":
1. ✅ Se crea automáticamente una `Invoice` en estado "Abierto"
2. ✅ El importe se suma al `debt_balance` del `Partner`

### 📦 Control de Stock
Cada vez que se guarda un `PosOrderLine`:
1. ✅ Se resta automáticamente la cantidad del `StockQuant` correspondiente
2. ✅ Si no existe stock para ese producto/almacén, se crea con cantidad negativa

### 💰 Registro de Pagos
Cuando se crea un `Payment`:
1. ✅ Se resta el monto del `debt_balance` del `Partner`
2. ✅ Si el total pagado cubre el monto de la factura, ésta se marca como "Pagado"

## 📋 Ejemplos de Uso con curl

### Crear un Partner (Cliente)

### Crear un Partner (Cliente)
```bash
curl -X POST http://127.0.0.1:8000/api/partners/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Homer Simpson",
    "is_supplier": false
  }'
```

### Crear un Producto
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cerveza Duff",
    "sales_price": "5.50"
  }'
```

### Crear un Almacén
```bash
curl -X POST http://127.0.0.1:8000/api/warehouses/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Barra Principal"
  }'
```

### Crear Stock Inicial
```bash
curl -X POST http://127.0.0.1:8000/api/stock-quants/ \
  -H "Content-Type: application/json" \
  -d '{
    "product": "UUID_DEL_PRODUCTO",
    "location": "UUID_DEL_ALMACEN",
    "quantity": "100"
  }'
```

### Crear un Ticket de Venta (POS Order)
```bash
curl -X POST http://127.0.0.1:8000/api/pos-orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer": "UUID_DEL_CLIENTE",
    "warehouse": "UUID_DEL_ALMACEN",
    "state": "draft",
    "lines": [
      {
        "product": "UUID_DEL_PRODUCTO",
        "qty": 3,
        "price_subtotal": "16.50"
      }
    ]
  }'
```

### Marcar Ticket como Fiado (Genera Factura Automática)
```bash
curl -X POST http://127.0.0.1:8000/api/pos-orders/UUID_DEL_TICKET/mark_debt/ \
  -H "Content-Type: application/json"
```

### Registrar un Pago
```bash
curl -X POST http://127.0.0.1:8000/api/payments/ \
  -H "Content-Type: application/json" \
  -d '{
    "invoice": "UUID_DE_LA_FACTURA",
    "amount": "16.50",
    "method": "cash"
  }'
```

### Crear Orden de Compra
```bash
curl -X POST http://127.0.0.1:8000/api/purchase-orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "supplier": "UUID_DEL_PROVEEDOR",
    "state": "draft",
    "lines": [
      {
        "product": "UUID_DEL_PRODUCTO",
        "quantity": 50
      }
    ]
  }'
```

### Crear un Empleado
```bash
curl -X POST http://127.0.0.1:8000/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Moe Szyslak",
    "job_title": "Propietario y Bartender"
  }'
```

### Ver Deudas de un Cliente
```bash
curl http://127.0.0.1:8000/api/partners/UUID_DEL_CLIENTE/debt_history/
```

### Listar Facturas Abiertas
```bash
curl http://127.0.0.1:8000/api/invoices/open_invoices/
```

### Ver Inventario de un Almacén
```bash
curl http://127.0.0.1:8000/api/warehouses/UUID_DEL_ALMACEN/inventory/
```

## 🧪 Prueba Rápida

Ejecutar script para verificar que la base de datos funciona:
```bash
python scripts/smoke_test.py
```

Probar el modelo de facturas legacy:
```bash
python scripts/test_facturas.py
```

## 🚀 Características Avanzadas

### Gestión Automática de Deudas
- Al marcar un ticket como "Fiado", se genera automáticamente una factura
- La deuda se registra en el balance del cliente
- Los pagos se descuentan automáticamente de la deuda

### Control de Inventario en Tiempo Real
- Cada venta reduce automáticamente el stock
- Consulta de stock por producto y almacén
- Soporte para múltiples almacenes

### Trazabilidad Completa
- Todas las transacciones quedan registradas
- Las facturas mantienen referencia al ticket original
- Historial de pagos por factura

### Panel de Administración
Accede a **http://127.0.0.1:8000/admin/** para:
- Gestionar todos los modelos visualmente
- Ver reportes y relaciones
- Editar datos de forma intuitiva

## 📊 Campos de Modelos

### Partner
- `id`: UUID automático
- `name`: Nombre del socio/cliente/proveedor
- `is_supplier`: Boolean (True = Proveedor)
- `debt_balance`: Deuda acumulada (se actualiza automáticamente)

### Product
- `id`: UUID automático
- `name`: Nombre del producto
- `sales_price`: Precio de venta

### PurchaseOrder
- `id`: UUID automático
- `supplier`: FK a Partner (solo proveedores)
- `date_order`: Fecha automática
- `state`: draft | confirmed

### Warehouse
- `id`: UUID automático
- `name`: Nombre del almacén

### StockQuant
- `id`: UUID automático
- `product`: FK a Product
- `location`: FK a Warehouse
- `quantity`: Cantidad en stock

### PosOrder
- `id`: UUID automático
- `session_id`: Referencia de sesión (opcional)
- `customer`: FK a Partner (opcional)
- `warehouse`: FK a Warehouse
- `date`: Fecha automática
- `state`: draft | paid | debt

### Invoice
- `id`: UUID automático
- `origin`: Referencia (ej: "POS-ABC123")
- `partner`: FK a Partner
- `amount_total`: Monto total
- `state`: open | paid
- `due_date`: Fecha de vencimiento

### Payment
- `id`: UUID automático
- `invoice`: FK a Invoice
- `amount`: Monto del pago
- `method`: cash | check | kind
- `date`: Fecha automática

### Employee
- `id`: UUID automático
- `name`: Nombre del empleado
- `job_title`: Cargo/Puesto

---

**¡Sistema completo de gestión para la Taberna de Moe!** 🍺✨