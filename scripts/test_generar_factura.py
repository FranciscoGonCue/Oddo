"""
Script de prueba para generar una factura con PDF
"""
import os
import sys
import django

# Agregar el directorio padre al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SECRET_KEY', 'change-me-for-production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oddo_project.settings')
django.setup()

from core.models import Socio, Producto
from invoicing.models import Factura, LineaFactura, ConfiguracionEmpresa
from decimal import Decimal

def crear_factura_ejemplo():
    """Crear una factura de ejemplo con el formato mostrado"""
    
    # 1. Configurar datos de la empresa si no existen
    config = ConfiguracionEmpresa.get_config()
    print(f"✅ Configuración de empresa: {config.nombre}")
    
    # 2. Obtener o crear un socio cliente
    cliente, _ = Socio.objects.get_or_create(
        nombre="Gemini Furniture",
        defaults={
            'es_proveedor': False,
            'saldo_deuda': Decimal('0.00')
        }
    )
    print(f"✅ Cliente: {cliente.nombre}")
    
    # 3. Crear productos si no existen
    productos = [
        {
            'codigo': 'FURN 6667',
            'nombre': 'Pantallas acústicas (Negro)',
            'descripcion': 'Paneles que reducen el ruido para espacios abiertos',
            'precio': Decimal('295.00'),
            'cantidad': Decimal('5.00')
        },
        {
            'codigo': '',
            'nombre': 'Sofá de dos plazas (Lino)',
            'descripcion': 'Sofá de dos plazas con estructura de madera de roble',
            'precio': Decimal('173.00'),
            'cantidad': Decimal('1.00')
        },
        {
            'codigo': 'FURN 8888',
            'nombre': 'Lámpara de oficina',
            'descripcion': 'Lámpara de oficina',
            'precio': Decimal('40.00'),
            'cantidad': Decimal('1.00')
        },
        {
            'codigo': 'FURN 7777',
            'nombre': 'Silla de oficina',
            'descripcion': 'Una cómoda silla amarilla para uso diario',
            'precio': Decimal('18.00'),
            'cantidad': Decimal('1.00')
        },
    ]
    
    # Crear productos en la base de datos
    for prod_data in productos:
        if prod_data['nombre']:
            Producto.objects.get_or_create(
                nombre=prod_data['nombre'],
                defaults={'precio_venta': prod_data['precio']}
            )
    
    print(f"✅ Productos creados/verificados")
    
    # 4. Crear la factura
    factura = Factura.objects.create(
        socio=cliente,
        vendedor="Mitchell Admin",
        cliente_nombre="Gemini Furniture",
        cliente_direccion="Via Industria 21",
        cliente_ciudad="Serravalle 47899",
        cliente_identificacion="Número de identificación fiscal: SM12345",
        monto_total=Decimal('1706.00'),
        tasa_impuesto=Decimal('0.00'),  # 0% Exportaciones
        estado='abierto'
    )
    
    print(f"✅ Factura creada: {factura.numero_orden}")
    
    # 5. Crear las líneas de la factura
    for prod_data in productos:
        producto = Producto.objects.filter(nombre=prod_data['nombre']).first()
        
        LineaFactura.objects.create(
            factura=factura,
            producto=producto,
            codigo_producto=prod_data['codigo'],
            descripcion=prod_data['descripcion'],
            cantidad=prod_data['cantidad'],
            precio_unitario=prod_data['precio'],
            tasa_impuesto=Decimal('0.00')
        )
    
    print(f"✅ {factura.lineas.count()} líneas de factura creadas")
    
    # 6. Generar el PDF
    from invoicing.pdf_generator import generar_pdf_factura
    from django.core.files.base import ContentFile
    
    try:
        pdf_buffer = generar_pdf_factura(factura)
        pdf_filename = f'factura_{factura.numero_orden}.pdf'
        factura.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)
        print(f"✅ PDF generado: {factura.pdf_file.path}")
        print(f"📄 Puedes encontrar el PDF en: {factura.pdf_file.path}")
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
    
    # 7. Mostrar resumen
    print("\n" + "="*60)
    print(f"FACTURA GENERADA EXITOSAMENTE")
    print("="*60)
    print(f"Número de orden: {factura.numero_orden}")
    print(f"Cliente: {factura.cliente_nombre}")
    print(f"Total: ${factura.monto_total}")
    print(f"Estado: {factura.get_estado_display()}")
    print(f"Fecha: {factura.fecha_creacion.strftime('%d/%m/%Y')}")
    print(f"\nLíneas de factura:")
    for linea in factura.lineas.all():
        print(f"  - {linea.descripcion}: {linea.cantidad} × ${linea.precio_unitario} = ${linea.importe}")
    
    if factura.pdf_file:
        print(f"\n📄 PDF disponible en: /api/facturas/{factura.id}/descargar_pdf/")
        print(f"   Archivo local: {factura.pdf_file.path}")
    
    return factura

if __name__ == '__main__':
    print("🚀 Creando factura de ejemplo...\n")
    factura = crear_factura_ejemplo()
    print("\n✨ ¡Listo!")
