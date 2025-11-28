from django.db import models
import uuid
from core.models import Producto


# =============================================================================
# 🏭 MÓDULO INVENTARIO (Inventory)
# =============================================================================

class Almacen(models.Model):
    """Lugares físicos donde se almacena mercancía"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, help_text="Ej: 'Barra', 'Trastienda'")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"
        ordering = ['nombre']

    def __str__(self):
        return f"📍 {self.nombre}"


class CantidadStock(models.Model):
    """Stock real en mano"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='cantidades_stock')
    ubicacion = models.ForeignKey(Almacen, on_delete=models.PROTECT, related_name='cantidades_stock')
    cantidad = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0.00,
        help_text="Cantidad real ahora mismo"
    )
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cantidad de Stock"
        verbose_name_plural = "Cantidades de Stock"
        unique_together = ['producto', 'ubicacion']

    def __str__(self):
        return f"{self.producto.nombre} @ {self.ubicacion.nombre}: {self.cantidad}"
