from django.db import models
from django.db.models import Sum
import uuid
from decimal import Decimal
from core.models import Socio, Producto
from inventory.models import Almacen, CantidadStock


# =============================================================================
# 🖥️ MÓDULO PUNTO DE VENTA (POS)
# =============================================================================

class OrdenPOS(models.Model):
    """El ticket de venta"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('pagado', 'Pagado'),
        ('fiado', 'Fiado/Deuda'),
    ]
    
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('tarjeta', 'Tarjeta'),
        ('transferencia', 'Transferencia'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_sesion = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Referencia externa de sesión"
    )
    sesion_mesa = models.ForeignKey(
        'mesas.SesionMesa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordenes',
        help_text="Sesión de mesa asociada"
    )
    cliente = models.ForeignKey(
        Socio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ordenes_pos'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')
    metodo_pago = models.CharField(
        max_length=20, 
        choices=METODO_PAGO_CHOICES, 
        blank=True, 
        null=True,
        help_text="Método de pago utilizado"
    )
    almacen = models.ForeignKey(
        Almacen,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Almacén desde donde se vende"
    )

    class Meta:
        verbose_name = "Orden POS (Ticket de Venta)"
        verbose_name_plural = "Órdenes POS"
        ordering = ['-fecha']

    def __str__(self):
        nombre_cliente = self.cliente.nombre if self.cliente else "Cliente General"
        return f"POS-{str(self.id)[:8]} - {nombre_cliente} [{self.get_estado_display()}]"

    def obtener_total(self):
        """Calcula el total del ticket"""
        total = self.lineas.aggregate(total=Sum('precio_subtotal'))['total']
        return total or Decimal('0.00')

    def save(self, *args, **kwargs):
        """Lógica especial al guardar"""
        is_new = self.pk is None
        estado_anterior = None
        
        # Solo obtener el estado anterior si el objeto ya existe en la BD
        if not is_new:
            try:
                estado_anterior = OrdenPOS.objects.get(pk=self.pk).estado
            except OrdenPOS.DoesNotExist:
                estado_anterior = None
        
        super().save(*args, **kwargs)
        
        # Si cambia a "Fiado/Deuda", crear factura automáticamente con PDF
        if self.estado == 'fiado' and estado_anterior != 'fiado' and self.cliente:
            from invoicing.models import Factura, LineaFactura
            from django.core.files.base import ContentFile
            
            total = self.obtener_total()
            if total > 0:
                # Crear factura
                factura = Factura.objects.create(
                    origen=f"POS-{str(self.id)[:8]}",
                    socio=self.cliente,
                    vendedor="Sistema POS",
                    cliente_nombre=self.cliente.nombre,
                    monto_total=total,
                    tasa_impuesto=Decimal('0.00'),
                    estado='abierto'
                )
                
                # Crear líneas de factura desde las líneas del POS
                for linea in self.lineas.all():
                    LineaFactura.objects.create(
                        factura=factura,
                        producto=linea.producto,
                        codigo_producto=f"PROD-{linea.producto.id}",
                        descripcion=linea.producto.nombre,
                        cantidad=linea.cantidad,
                        precio_unitario=linea.precio_unitario,
                        tasa_impuesto=Decimal('0.00')
                    )
                
                # Generar el PDF automáticamente
                try:
                    from invoicing.pdf_generator import generar_pdf_factura
                    pdf_buffer = generar_pdf_factura(factura)
                    pdf_filename = f'factura_{factura.numero_orden}.pdf'
                    factura.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)
                except Exception as e:
                    print(f"Error generando PDF para factura {factura.numero_orden}: {e}")
                
                # Actualizar deuda del socio
                self.cliente.saldo_deuda = Decimal(str(self.cliente.saldo_deuda)) + total
                self.cliente.save()


class LineaOrdenPOS(models.Model):
    """Líneas del ticket"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden_pos = models.ForeignKey(OrdenPOS, on_delete=models.CASCADE, related_name='lineas')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1, help_text="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Precio unitario en el momento de la venta")
    precio_subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Línea de Orden POS"
        verbose_name_plural = "Líneas de Órdenes POS"

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad} = ${self.precio_subtotal}"

    def save(self, *args, **kwargs):
        """Calcular subtotal y reducir stock automáticamente"""
        # Guardar precio unitario si no está definido
        if not self.precio_unitario or self.precio_unitario == 0:
            self.precio_unitario = self.producto.precio_venta
        
        # Calcular precio subtotal
        if not self.precio_subtotal or self.precio_subtotal == 0:
            self.precio_subtotal = self.precio_unitario * self.cantidad
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Reducir stock si es una nueva línea y hay almacen definido
        if is_new and self.orden_pos.almacen:
            try:
                stock = CantidadStock.objects.get(
                    producto=self.producto,
                    ubicacion=self.orden_pos.almacen
                )
                stock.cantidad -= self.cantidad
                stock.save()
            except CantidadStock.DoesNotExist:
                # Crear stock negativo si no existe
                CantidadStock.objects.create(
                    producto=self.producto,
                    ubicacion=self.orden_pos.almacen,
                    cantidad=-self.cantidad
                )
