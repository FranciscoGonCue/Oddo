from django.db import models
from django.db.models import Sum
from django.conf import settings
import uuid
from decimal import Decimal
from core.models import Socio, Producto
import os


# =============================================================================
# 📄 MÓDULO FACTURACIÓN (Invoicing)
# =============================================================================

class ConfiguracionEmpresa(models.Model):
    """Configuración de datos de la empresa para facturas"""
    nombre = models.CharField(max_length=200, default="YourCompany")
    direccion_linea1 = models.CharField(max_length=200, default="8000 Marina Blvd. Suite 300")
    direccion_linea2 = models.CharField(max_length=200, default="94005 Brisbane")
    direccion_linea3 = models.CharField(max_length=200, default="California")
    direccion_linea4 = models.CharField(max_length=200, default="España")
    
    direccion_facturacion_nombre = models.CharField(max_length=200, default="Gemini Furniture. Soham Palmer")
    direccion_facturacion_linea1 = models.CharField(max_length=200, default="Via Industria 21")
    direccion_facturacion_linea2 = models.CharField(max_length=200, default="Serravalle 47899")
    direccion_facturacion_linea3 = models.CharField(max_length=200, default="San Marino")
    telefono_facturacion = models.CharField(max_length=50, default="(379)-167-2040")
    
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Configuración de Empresa"
        verbose_name_plural = "Configuración de Empresa"
    
    def __str__(self):
        return self.nombre
    
    @classmethod
    def get_config(cls):
        """Obtener o crear la configuración"""
        config, _ = cls.objects.get_or_create(pk=1)
        return config


class Factura(models.Model):
    """La cuenta formal"""
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('pagado', 'Pagado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_orden = models.CharField(max_length=50, unique=True, null=True, blank=True, help_text="Número de orden (ej: S00007)")
    origen = models.CharField(max_length=200, blank=True, help_text="Ej: 'POS/Ticket-001'")
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT, related_name='facturas')
    vendedor = models.CharField(max_length=200, blank=True, default="Mitchell Admin")
    
    # Datos del cliente en la factura
    cliente_nombre = models.CharField(max_length=200, blank=True, default="")
    cliente_direccion = models.CharField(max_length=200, blank=True)
    cliente_ciudad = models.CharField(max_length=200, blank=True)
    cliente_identificacion = models.CharField(max_length=100, blank=True)
    
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Porcentaje de impuesto")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    fecha_vencimiento = models.DateField(null=True, blank=True, help_text="Fecha de vencimiento")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Archivo PDF generado
    pdf_file = models.FileField(upload_to='facturas/', null=True, blank=True)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"FAC-{self.numero_orden} - {self.socio.nombre} - ${self.monto_total} [{self.get_estado_display()}]"
    
    def save(self, *args, **kwargs):
        # Generar número de orden si no existe
        if not self.numero_orden:
            ultimo = Factura.objects.all().order_by('-fecha_creacion').first()
            if ultimo and ultimo.numero_orden and ultimo.numero_orden.startswith('S'):
                try:
                    num = int(ultimo.numero_orden[1:]) + 1
                except:
                    num = 1
            else:
                num = 1
            self.numero_orden = f'S{num:05d}'
        
        # Copiar datos del socio si no están presentes
        if not self.cliente_nombre:
            self.cliente_nombre = self.socio.nombre
        
        super().save(*args, **kwargs)


class LineaFactura(models.Model):
    """Líneas de detalle de una factura"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    codigo_producto = models.CharField(max_length=50, blank=True, help_text="Código del producto (ej: FURN 6667)")
    descripcion = models.TextField(help_text="Descripción del producto/servicio")
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="% de impuesto")
    importe = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cantidad × Precio unitario")
    
    class Meta:
        verbose_name = "Línea de Factura"
        verbose_name_plural = "Líneas de Factura"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} × ${self.precio_unitario}"
    
    def save(self, *args, **kwargs):
        # Calcular importe
        self.importe = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


class Pago(models.Model):
    """El registro del pago"""
    METODO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
        ('cheque', 'Cheque'),
        ('especie', 'Especie'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='pagos')
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, default='efectivo')
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Pago ${self.monto} - {self.get_metodo_display()}"

    def save(self, *args, **kwargs):
        """Al registrar un pago, actualizar factura y deuda del socio"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            # Reducir deuda del socio
            self.factura.socio.saldo_deuda = Decimal(str(self.factura.socio.saldo_deuda)) - self.monto
            self.factura.socio.save()
            
            # Verificar si la factura está totalmente pagada
            total_pagado = self.factura.pagos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
            if total_pagado >= self.factura.monto_total:
                self.factura.estado = 'pagado'
                self.factura.save()
