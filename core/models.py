from django.db import models
import uuid


# =============================================================================
# 📦 MÓDULO CORE (Base)
# =============================================================================

class Socio(models.Model):
    """Socios, Clientes y Proveedores de la Taberna de Moe"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, help_text="Nombre del socio/cliente/proveedor")
    es_proveedor = models.BooleanField(default=False, help_text="¿Es proveedor? (Ej: Duff)")
    saldo_deuda = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Cuenta pendiente (la deuda de Homer)"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Socio (Cliente/Proveedor)"
        verbose_name_plural = "Socios"
        ordering = ['nombre']

    def __str__(self):
        tipo = "🍺 Proveedor" if self.es_proveedor else "👤 Cliente"
        return f"{tipo}: {self.nombre} (Deuda: ${self.saldo_deuda})"


class Producto(models.Model):
    """Bebidas y comida de la taberna"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, help_text="Nombre del producto")
    precio_venta = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Precio de venta"
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - ${self.precio_venta}"
