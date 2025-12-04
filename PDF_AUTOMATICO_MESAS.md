# Guía: Generación Automática de PDF al Cerrar Mesa

## ✨ Qué se ha implementado

Ahora, cuando cierras una mesa (sesión de mesa), el sistema automáticamente:

1. ✅ Crea una factura con todas las órdenes de la mesa
2. ✅ Genera líneas de factura con los detalles de los productos
3. ✅ Genera el PDF automáticamente con el formato corporativo
4. ✅ Registra el pago
5. ✅ Marca la factura como pagada

## 🚀 Cómo funciona

### Al cerrar una mesa con cliente:

```bash
POST /mesas/mesas/{id_mesa}/cerrar/
{
  "metodo_pago": "efectivo"  # o "tarjeta" o "transferencia"
}
```

**Respuesta**:
```json
{
  "mesa": { ... },
  "ordenes_procesadas": 3,
  "metodo_pago": "efectivo",
  "total": "1475.00",
  "factura_id": "uuid-de-la-factura",
  "factura_numero": "S00002",
  "pdf_url": "http://localhost:8000/media/facturas/factura_S00002.pdf"
}
```

### Flujo completo:

1. **Abrir mesa**:
   ```javascript
   POST /mesas/mesas/{id}/abrir/
   {
     "numero_personas": 4,
     "cliente": "uuid-del-cliente",  // IMPORTANTE: Debe tener cliente
     "notas": "Mesa cerca de la ventana"
   }
   ```

2. **Agregar órdenes** (productos):
   ```javascript
   POST /api/ordenes-pos/
   {
     "sesion_mesa": "uuid-de-la-sesion",
     "lineas": [
       {
         "producto": "uuid-producto-1",
         "cantidad": 2
       },
       {
         "producto": "uuid-producto-2",
         "cantidad": 1
       }
     ]
   }
   ```

3. **Ver cuenta** (opcional):
   ```javascript
   GET /mesas/mesas/{id}/cuenta/
   ```

4. **Cerrar mesa** (genera factura + PDF):
   ```javascript
   POST /mesas/mesas/{id}/cerrar/
   {
     "metodo_pago": "efectivo"
   }
   ```

## 📄 Contenido del PDF generado

El PDF incluye:
- **Encabezado**: Logo y datos de la empresa
- **Cliente**: Nombre y datos del socio
- **Número de orden**: Generado automáticamente (S00001, S00002, etc.)
- **Fecha y vendedor**: Información de la venta
- **Líneas de productos**: 
  - Código del producto
  - Descripción
  - Cantidad
  - Precio unitario
  - Impuestos
  - Importe total
- **Totales**: Subtotal, impuestos y total

## 🔄 También funciona con órdenes "Fiadas"

Si marcas una orden POS como "fiado" (deuda), también se genera automáticamente una factura con PDF:

```python
orden = OrdenPOS.objects.get(id=...)
orden.estado = 'fiado'
orden.save()  # Automáticamente genera factura + PDF
```

## 📁 Ubicación de los PDFs

Los PDFs se guardan en:
```
/media/facturas/factura_S00001.pdf
/media/facturas/factura_S00002.pdf
...
```

Accesibles vía:
```
http://localhost:8000/media/facturas/factura_S00001.pdf
```

O mediante el endpoint:
```
GET /api/facturas/{id}/descargar_pdf/
```

## ⚠️ Importante

- La mesa **DEBE tener un cliente asignado** para generar la factura
- Si la mesa no tiene cliente, se cierra pero NO se genera factura
- Las órdenes deben estar en estado "borrador" para ser procesadas
- Al cerrar la mesa, todas las órdenes pasan a estado "pagado"

## 🧪 Ejemplo de prueba completo

```python
import requests

base_url = "http://localhost:8000"

# 1. Obtener una mesa libre
mesas = requests.get(f"{base_url}/mesas/mesas/libres/").json()
mesa_id = mesas[0]['id']

# 2. Obtener un cliente
socios = requests.get(f"{base_url}/api/socios/").json()
cliente_id = socios['results'][0]['id']

# 3. Abrir la mesa
abrir = requests.post(
    f"{base_url}/mesas/mesas/{mesa_id}/abrir/",
    json={
        "numero_personas": 2,
        "cliente": cliente_id
    }
).json()

sesion_id = abrir['sesion']['id']

# 4. Obtener productos
productos = requests.get(f"{base_url}/api/productos/").json()
producto_1 = productos['results'][0]['id']
producto_2 = productos['results'][1]['id']

# 5. Crear orden con productos
orden = requests.post(
    f"{base_url}/api/ordenes-pos/",
    json={
        "sesion_mesa": sesion_id,
        "lineas": [
            {"producto": producto_1, "cantidad": 2},
            {"producto": producto_2, "cantidad": 1}
        ]
    }
).json()

# 6. Ver cuenta
cuenta = requests.get(f"{base_url}/mesas/mesas/{mesa_id}/cuenta/").json()
print(f"Total a pagar: ${cuenta['total']}")

# 7. Cerrar mesa (genera factura + PDF automáticamente)
cerrar = requests.post(
    f"{base_url}/mesas/mesas/{mesa_id}/cerrar/",
    json={"metodo_pago": "efectivo"}
).json()

print(f"Factura generada: {cerrar['factura_numero']}")
print(f"PDF disponible en: {cerrar['pdf_url']}")

# 8. Descargar el PDF
pdf_response = requests.get(cerrar['pdf_url'])
with open('factura_mesa.pdf', 'wb') as f:
    f.write(pdf_response.content)
print("PDF descargado como factura_mesa.pdf")
```

## 🎉 ¡Listo!

Ahora cada vez que cierres una mesa con cliente, se generará automáticamente un PDF de factura profesional con todos los detalles de la compra.
