from django.db import models
from django.db.models import Sum
import uuid
from decimal import Decimal
from core.models import Socio


# =============================================================================
# 📄 MÓDULO FACTURACIÓN (Invoicing)
# =============================================================================

class Factura(models.Model):
    """La cuenta formal"""
    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('pagado', 'Pagado'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    origen = models.CharField(max_length=200, blank=True, help_text="Ej: 'POS/Ticket-001'")
    socio = models.ForeignKey(Socio, on_delete=models.PROTECT, related_name='facturas')
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')
    fecha_vencimiento = models.DateField(null=True, blank=True, help_text="Fecha de vencimiento")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"FAC-{str(self.id)[:8]} - {self.socio.nombre} - ${self.monto_total} [{self.get_estado_display()}]"


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
