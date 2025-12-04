from rest_framework import serializers
from django.db.models import Sum
from django.core.files.base import ContentFile
from decimal import Decimal
from .models import Factura, Pago, LineaFactura
from .pdf_generator import generar_pdf_factura


class LineaFacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineaFactura
        fields = ['id', 'producto', 'codigo_producto', 'descripcion', 'cantidad', 
                  'precio_unitario', 'tasa_impuesto', 'importe']
        read_only_fields = ['id', 'importe']


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'factura', 'monto', 'metodo', 'fecha']
        read_only_fields = ['id', 'fecha']


class FacturaSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.CharField(source='socio.nombre', read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)
    lineas = LineaFacturaSerializer(many=True, required=False)
    total_pagado = serializers.SerializerMethodField()
    restante = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Factura
        fields = ['id', 'numero_orden', 'origen', 'socio', 'nombre_socio', 'vendedor',
                  'cliente_nombre', 'cliente_direccion', 'cliente_ciudad', 'cliente_identificacion',
                  'monto_total', 'tasa_impuesto', 'estado', 
                  'fecha_vencimiento', 'fecha_creacion', 'pagos', 'lineas',
                  'total_pagado', 'restante', 'pdf_file', 'pdf_url']
        read_only_fields = ['id', 'numero_orden', 'fecha_creacion', 'pdf_file']
    
    def get_total_pagado(self, obj):
        total = obj.pagos.aggregate(total=Sum('monto'))['total']
        return str(total or Decimal('0.00'))
    
    def get_restante(self, obj):
        total_pagado = obj.pagos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        restante = obj.monto_total - total_pagado
        return str(restante)
    
    def get_pdf_url(self, obj):
        if obj.pdf_file:
            return obj.pdf_file.url
        return None
    
    def create(self, validated_data):
        # Extraer las líneas si existen
        lineas_data = validated_data.pop('lineas', [])
        
        # Crear la factura
        factura = Factura.objects.create(**validated_data)
        
        # Crear las líneas de factura
        for linea_data in lineas_data:
            LineaFactura.objects.create(factura=factura, **linea_data)
        
        # Generar el PDF automáticamente
        try:
            pdf_buffer = generar_pdf_factura(factura)
            pdf_filename = f'factura_{factura.numero_orden}.pdf'
            factura.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)
        except Exception as e:
            # Si falla la generación del PDF, registrar el error pero no fallar la creación
            print(f"Error generando PDF: {e}")
        
        return factura
    
    def update(self, instance, validated_data):
        # Extraer las líneas si existen
        lineas_data = validated_data.pop('lineas', None)
        
        # Actualizar la factura
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Si se proporcionaron líneas, actualizarlas
        if lineas_data is not None:
            # Eliminar líneas existentes
            instance.lineas.all().delete()
            
            # Crear nuevas líneas
            for linea_data in lineas_data:
                LineaFactura.objects.create(factura=instance, **linea_data)
            
            # Regenerar el PDF
            try:
                pdf_buffer = generar_pdf_factura(instance)
                pdf_filename = f'factura_{instance.numero_orden}.pdf'
                instance.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)
            except Exception as e:
                print(f"Error regenerando PDF: {e}")
        
        return instance
