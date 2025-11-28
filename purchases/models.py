from django.db import models
import uuid
from core.models import Socio, Producto


# =============================================================================
# 🛒 MÓDULO COMPRAS (Purchase)
# =============================================================================

class OrdenCompra(models.Model):
    """Cabecera del pedido de compra (para reponer barriles)"""
    ESTADO_CHOICES = [
        ('borrador', 'Borrador'),
        ('confirmado', 'Confirmado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    proveedor = models.ForeignKey(
        Socio, 
        on_delete=models.PROTECT,
        limit_choices_to={'es_proveedor': True},
        related_name='ordenes_compra',
        help_text="Proveedor"
    )
    fecha_orden = models.DateTimeField(auto_now_add=True, help_text="Fecha del pedido")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='borrador')

    class Meta:
        verbose_name = "Orden de Compra"
        verbose_name_plural = "Órdenes de Compra"
        ordering = ['-fecha_orden']

    def __str__(self):
        return f"OC-{str(self.id)[:8]} - {self.proveedor.nombre} [{self.get_estado_display()}]"


class LineaOrdenCompra(models.Model):
    """Detalle del pedido de compra"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orden_compra = models.ForeignKey(
        OrdenCompra,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField(default=1, help_text="Cantidad (Ej. 10 barriles)")

    class Meta:
        verbose_name = "Línea de Orden de Compra"
        verbose_name_plural = "Líneas de Órdenes de Compra"

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"
