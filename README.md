# Proyecto Django API básica

_Ejemplo mínimo de API con Django + Django REST Framework._

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
python manage.py makemigrations api
python manage.py migrate
```

5. **Ejecutar servidor:**
```bash
python manage.py runserver
```

El servidor estará disponible en: **http://127.0.0.1:8000/**

## Endpoints API

- `GET/POST /api/items/` - Listar/crear items
- `GET/PUT/PATCH/DELETE /api/items/{id}/` - Operaciones con item específico
- `GET/POST /api/facturas/` - Listar/crear facturas  
- `GET/PUT/PATCH/DELETE /api/facturas/{id}/` - Operaciones con factura específica

### Modelo de Facturas

Las facturas incluyen los siguientes campos:
- **direccion**: Dirección de facturación (texto)
- **cliente**: Nombre del cliente (texto)
- **vendedor**: Nombre del vendedor (texto)
- **fecha_creacion**: Fecha y hora de creación (automática)
- **cantidad_dinero**: Cantidad en formato decimal (ej: 1234.56)

## Prueba rápida

Ejecutar script para verificar que la base de datos funciona:
```bash
python scripts/smoke_test.py
```

Probar el modelo de facturas:
```bash
python scripts/test_facturas.py
```

## Ejemplo de uso con curl

```bash
# Crear un item
curl -X POST http://127.0.0.1:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Mi item", "description": "Descripción del item"}'

# Listar items
curl http://127.0.0.1:8000/api/items/

# Crear una factura
curl -X POST http://127.0.0.1:8000/api/facturas/ \
  -H "Content-Type: application/json" \
  -d '{
    "direccion": "Calle Mayor 123, Madrid, España",
    "cliente": "Juan Pérez", 
    "vendedor": "María García",
    "cantidad_dinero": "1250.75"
  }'

# Listar facturas
curl http://127.0.0.1:8000/api/facturas/
```

Proyecto listo para desarrollo y extensión! 🚀