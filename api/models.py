from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Factura(models.Model):
    direccion = models.CharField(max_length=500, help_text="Dirección de facturación")
    cliente = models.CharField(max_length=200, help_text="Nombre del cliente")
    vendedor = models.CharField(max_length=200, help_text="Nombre del vendedor")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    cantidad_dinero = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        help_text="Cantidad en formato decimal (ej: 1234.56)"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente} - ${self.cantidad_dinero}"
