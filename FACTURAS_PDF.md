# Generación Automática de PDFs para Facturas

## 📋 Descripción

El sistema ahora genera automáticamente archivos PDF descargables para las facturas cuando se crean, siguiendo el formato proporcionado.

## ✨ Características

- **Generación automática**: El PDF se crea automáticamente al crear una factura
- **Formato personalizado**: Incluye logo de empresa, datos del cliente, líneas de productos, impuestos y totales
- **Descargable**: Archivos PDF almacenados y disponibles para descarga
- **API completa**: Endpoints REST para crear facturas con líneas de detalle

## 🗂️ Modelos Actualizados

### ConfiguracionEmpresa
Almacena la información de la empresa que aparece en las facturas:
- Nombre y dirección de la empresa
- Dirección de facturación y envío
- Logo (opcional)

### Factura
Campos principales:
- `numero_orden`: Generado automáticamente (S00001, S00002, etc.)
- `socio`: Cliente/Proveedor
- `vendedor`: Nombre del vendedor
- `cliente_nombre`, `cliente_direccion`, `cliente_ciudad`, `cliente_identificacion`: Datos del cliente
- `monto_total`: Total de la factura
- `tasa_impuesto`: Porcentaje de impuesto
- `pdf_file`: Archivo PDF generado

### LineaFactura
Líneas de detalle de cada factura:
- `producto`: Referencia al producto (opcional)
- `codigo_producto`: Código del producto (ej: FURN 6667)
- `descripcion`: Descripción del producto/servicio
- `cantidad`: Cantidad de unidades
- `precio_unitario`: Precio por unidad
- `tasa_impuesto`: Porcentaje de impuesto
- `importe`: Calculado automáticamente (cantidad × precio_unitario)

## 🚀 Uso

### 1. Configurar Datos de la Empresa

Accede al admin de Django:
```
http://localhost:8000/admin/invoicing/configuracionempresa/
```

Configura:
- Nombre de la empresa
- Direcciones
- Logo (opcional)

### 2. Crear Factura con la API

**Endpoint**: `POST /api/facturas/`

**Ejemplo de petición**:
```json
{
  "socio": "uuid-del-socio",
  "vendedor": "Mitchell Admin",
  "cliente_nombre": "Gemini Furniture",
  "cliente_direccion": "Via Industria 21",
  "cliente_ciudad": "Serravalle 47899",
  "cliente_identificacion": "Número de identificación fiscal: SM12345",
  "monto_total": 1706.00,
  "tasa_impuesto": 0.00,
  "lineas": [
    {
      "codigo_producto": "FURN 6667",
      "descripcion": "Paneles que reducen el ruido para espacios abiertos",
      "cantidad": 5.00,
      "precio_unitario": 295.00,
      "tasa_impuesto": 0.00
    },
    {
      "codigo_producto": "",
      "descripcion": "Sofá de dos plazas con estructura de madera de roble",
      "cantidad": 1.00,
      "precio_unitario": 173.00,
      "tasa_impuesto": 0.00
    }
  ]
}
```

El PDF se genera automáticamente al crear la factura.

### 3. Descargar el PDF

**Endpoint**: `GET /api/facturas/{id}/descargar_pdf/`

O accede directamente al campo `pdf_url` en la respuesta de la API.

### 4. Crear Factura desde el Admin

También puedes crear facturas desde el admin de Django:
```
http://localhost:8000/admin/invoicing/factura/add/
```

Agrega líneas de factura usando el inline editor.

## 📊 Endpoints de la API

- `GET /api/facturas/` - Listar facturas
- `POST /api/facturas/` - Crear factura (genera PDF automáticamente)
- `GET /api/facturas/{id}/` - Detalle de factura
- `PUT /api/facturas/{id}/` - Actualizar factura (regenera PDF)
- `DELETE /api/facturas/{id}/` - Eliminar factura
- `GET /api/facturas/{id}/descargar_pdf/` - Descargar PDF
- `GET /api/facturas/facturas_abiertas/` - Listar facturas pendientes

- `GET /api/lineas-factura/` - Listar líneas de factura
- `POST /api/lineas-factura/` - Crear línea de factura
- `GET /api/lineas-factura/{id}/` - Detalle de línea
- `PUT /api/lineas-factura/{id}/` - Actualizar línea
- `DELETE /api/lineas-factura/{id}/` - Eliminar línea

- `GET /api/pagos/` - Listar pagos
- `POST /api/pagos/` - Registrar pago

## 🧪 Probar la Funcionalidad

Ejecuta el script de prueba:
```bash
python3 scripts/test_generar_factura.py
```

Esto creará una factura de ejemplo con PDF incluido.

## 📁 Ubicación de los PDFs

Los archivos PDF se guardan en:
```
/media/facturas/factura_S00001.pdf
```

Accesibles vía:
```
http://localhost:8000/media/facturas/factura_S00001.pdf
```

## 🔧 Instalación de Dependencias

Las siguientes dependencias fueron agregadas:
```
reportlab>=4.0.0
Pillow>=10.0.0
```

Instálalas con:
```bash
pip install -r requirements.txt
```

## 📝 Notas

- El número de orden se genera automáticamente con formato S00001, S00002, etc.
- Si no se especifica `cliente_nombre`, se copia del `socio`
- Los PDFs se regeneran automáticamente al actualizar una factura
- Los totales se calculan automáticamente en base a las líneas
