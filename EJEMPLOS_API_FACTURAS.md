# Ejemplos de Uso de la API de Facturas

## 📝 Crear una Factura Completa con Líneas

### Usando cURL:

```bash
curl -X POST http://localhost:8000/api/facturas/ \
  -H "Content-Type: application/json" \
  -d '{
    "socio": "UUID_DEL_SOCIO",
    "vendedor": "Mitchell Admin",
    "cliente_nombre": "Gemini Furniture",
    "cliente_direccion": "Via Industria 21",
    "cliente_ciudad": "Serravalle 47899",
    "cliente_identificacion": "Número de identificación fiscal: SM12345",
    "monto_total": 1706.00,
    "tasa_impuesto": 0.00,
    "estado": "abierto",
    "lineas": [
      {
        "codigo_producto": "FURN 6667",
        "descripcion": "Paneles que reducen el ruido para espacios abiertos",
        "cantidad": 5.00,
        "precio_unitario": 295.00,
        "tasa_impuesto": 0.00
      },
      {
        "descripcion": "Sofá de dos plazas con estructura de madera de roble",
        "cantidad": 1.00,
        "precio_unitario": 173.00,
        "tasa_impuesto": 0.00
      },
      {
        "codigo_producto": "FURN 8888",
        "descripcion": "Lámpara de oficina",
        "cantidad": 1.00,
        "precio_unitario": 40.00,
        "tasa_impuesto": 0.00
      },
      {
        "codigo_producto": "FURN 7777",
        "descripcion": "Una cómoda silla amarilla para uso diario",
        "cantidad": 1.00,
        "precio_unitario": 18.00,
        "tasa_impuesto": 0.00
      }
    ]
  }'
```

### Usando Python (requests):

```python
import requests
import json

url = "http://localhost:8000/api/facturas/"

# Primero, obtener el UUID de un socio
socios = requests.get("http://localhost:8000/api/socios/").json()
socio_id = socios['results'][0]['id']

# Datos de la factura
data = {
    "socio": socio_id,
    "vendedor": "Mitchell Admin",
    "cliente_nombre": "Gemini Furniture",
    "cliente_direccion": "Via Industria 21",
    "cliente_ciudad": "Serravalle 47899",
    "cliente_identificacion": "Número de identificación fiscal: SM12345",
    "monto_total": 1706.00,
    "tasa_impuesto": 0.00,
    "estado": "abierto",
    "lineas": [
        {
            "codigo_producto": "FURN 6667",
            "descripcion": "Paneles que reducen el ruido para espacios abiertos",
            "cantidad": 5.00,
            "precio_unitario": 295.00,
            "tasa_impuesto": 0.00
        },
        {
            "descripcion": "Sofá de dos plazas con estructura de madera de roble",
            "cantidad": 1.00,
            "precio_unitario": 173.00,
            "tasa_impuesto": 0.00
        },
        {
            "codigo_producto": "FURN 8888",
            "descripcion": "Lámpara de oficina",
            "cantidad": 1.00,
            "precio_unitario": 40.00,
            "tasa_impuesto": 0.00
        },
        {
            "codigo_producto": "FURN 7777",
            "descripcion": "Una cómoda silla amarilla para uso diario",
            "cantidad": 1.00,
            "precio_unitario": 18.00,
            "tasa_impuesto": 0.00
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())

# La respuesta incluirá el ID de la factura y la URL del PDF
factura = response.json()
print(f"Factura creada: {factura['numero_orden']}")
print(f"PDF disponible en: {factura['pdf_url']}")
```

### Usando JavaScript (fetch):

```javascript
const url = 'http://localhost:8000/api/facturas/';

// Primero, obtener el UUID de un socio
fetch('http://localhost:8000/api/socios/')
  .then(res => res.json())
  .then(data => {
    const socioId = data.results[0].id;
    
    // Datos de la factura
    const facturaData = {
      socio: socioId,
      vendedor: "Mitchell Admin",
      cliente_nombre: "Gemini Furniture",
      cliente_direccion: "Via Industria 21",
      cliente_ciudad: "Serravalle 47899",
      cliente_identificacion: "Número de identificación fiscal: SM12345",
      monto_total: 1706.00,
      tasa_impuesto: 0.00,
      estado: "abierto",
      lineas: [
        {
          codigo_producto: "FURN 6667",
          descripcion: "Paneles que reducen el ruido para espacios abiertos",
          cantidad: 5.00,
          precio_unitario: 295.00,
          tasa_impuesto: 0.00
        },
        {
          descripcion: "Sofá de dos plazas con estructura de madera de roble",
          cantidad: 1.00,
          precio_unitario: 173.00,
          tasa_impuesto: 0.00
        },
        {
          codigo_producto: "FURN 8888",
          descripcion: "Lámpara de oficina",
          cantidad: 1.00,
          precio_unitario: 40.00,
          tasa_impuesto: 0.00
        },
        {
          codigo_producto: "FURN 7777",
          descripcion: "Una cómoda silla amarilla para uso diario",
          cantidad: 1.00,
          precio_unitario: 18.00,
          tasa_impuesto: 0.00
        }
      ]
    };
    
    // Crear la factura
    return fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(facturaData)
    });
  })
  .then(res => res.json())
  .then(factura => {
    console.log('Factura creada:', factura.numero_orden);
    console.log('PDF disponible en:', factura.pdf_url);
  })
  .catch(error => console.error('Error:', error));
```

## 📥 Descargar el PDF de una Factura

### Usando cURL:

```bash
# Descargar el PDF
curl -o factura.pdf http://localhost:8000/api/facturas/UUID_DE_LA_FACTURA/descargar_pdf/

# O acceder directamente al archivo
curl -o factura.pdf http://localhost:8000/media/facturas/factura_S00001.pdf
```

### Usando Python:

```python
import requests

factura_id = "UUID_DE_LA_FACTURA"
url = f"http://localhost:8000/api/facturas/{factura_id}/descargar_pdf/"

response = requests.get(url)

with open('factura_descargada.pdf', 'wb') as f:
    f.write(response.content)

print("PDF descargado exitosamente")
```

### Usando JavaScript:

```javascript
const facturaId = 'UUID_DE_LA_FACTURA';
const url = `http://localhost:8000/api/facturas/${facturaId}/descargar_pdf/`;

fetch(url)
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'factura.pdf';
    document.body.appendChild(a);
    a.click();
    a.remove();
  });
```

## 📋 Listar Todas las Facturas

```bash
curl http://localhost:8000/api/facturas/
```

Respuesta:
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "UUID",
      "numero_orden": "S00001",
      "origen": "",
      "socio": "UUID_SOCIO",
      "nombre_socio": "Gemini Furniture",
      "vendedor": "Mitchell Admin",
      "cliente_nombre": "Gemini Furniture",
      "cliente_direccion": "Via Industria 21",
      "cliente_ciudad": "Serravalle 47899",
      "cliente_identificacion": "Número de identificación fiscal: SM12345",
      "monto_total": "1706.00",
      "tasa_impuesto": "0.00",
      "estado": "abierto",
      "fecha_vencimiento": null,
      "fecha_creacion": "2025-12-01T...",
      "pagos": [],
      "lineas": [...],
      "total_pagado": "0.00",
      "restante": "1706.00",
      "pdf_file": "/media/facturas/factura_S00001.pdf",
      "pdf_url": "http://localhost:8000/media/facturas/factura_S00001.pdf"
    }
  ]
}
```

## 💰 Registrar un Pago

```bash
curl -X POST http://localhost:8000/api/pagos/ \
  -H "Content-Type: application/json" \
  -d '{
    "factura": "UUID_DE_LA_FACTURA",
    "monto": 500.00,
    "metodo": "efectivo"
  }'
```

## 🔍 Ver Facturas Abiertas (Pendientes)

```bash
curl http://localhost:8000/api/facturas/facturas_abiertas/
```

## 🔄 Actualizar una Factura (Regenera el PDF)

```bash
curl -X PUT http://localhost:8000/api/facturas/UUID_DE_LA_FACTURA/ \
  -H "Content-Type: application/json" \
  -d '{
    "socio": "UUID_SOCIO",
    "vendedor": "Nuevo Vendedor",
    "cliente_nombre": "Cliente Actualizado",
    "monto_total": 2000.00,
    "lineas": [...]
  }'
```

El PDF se regenerará automáticamente con los nuevos datos.
