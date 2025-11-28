from django.db import models
import uuid
from decimal import Decimal


# =============================================================================
# 🪑 MÓDULO MESAS (Gestión de Mesas del Bar)
# =============================================================================

class Mesa(models.Model):
    """Mesas del bar/restaurante"""
    ESTADO_CHOICES = [
        ('libre', 'Libre'),
        ('ocupada', 'Ocupada'),
        ('reservada', 'Reservada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero = models.IntegerField(unique=True, help_text="Número de la mesa")
    capacidad = models.IntegerField(default=4, help_text="Número de personas")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='libre')
    posicion_x = models.IntegerField(default=0, help_text="Posición X en el plano")
    posicion_y = models.IntegerField(default=0, help_text="Posición Y en el plano")
    forma = models.CharField(
        max_length=20,
        choices=[('cuadrada', 'Cuadrada'), ('redonda', 'Redonda'), ('rectangular', 'Rectangular')],
        default='cuadrada'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mesa"
        verbose_name_plural = "Mesas"
        ordering = ['numero']

    def __str__(self):
        estado_emoji = {
            'libre': '🟢',
            'ocupada': '🔴',
            'reservada': '🟡'
        }
        return f"{estado_emoji.get(self.estado, '⚪')} Mesa {self.numero} ({self.capacidad} pers.) - {self.get_estado_display()}"

    def obtener_sesion_actual(self):
        """Obtiene la sesión actual activa de la mesa"""
        return self.sesiones.filter(estado='activa').first()
    
    def obtener_total_cuenta(self):
        """Obtiene el total de la cuenta actual"""
        sesion = self.obtener_sesion_actual()
        if sesion:
            return sesion.obtener_total()
        return Decimal('0.00')


class SesionMesa(models.Model):
    """Sesión de ocupación de una mesa"""
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cerrada', 'Cerrada'),
        ('cancelada', 'Cancelada'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='sesiones')
    cliente = models.ForeignKey(
        'core.Socio',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sesiones_mesa'
    )
    numero_personas = models.IntegerField(default=1, help_text="Número de comensales")
    hora_apertura = models.DateTimeField(auto_now_add=True)
    hora_cierre = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activa')
    notas = models.TextField(blank=True, help_text="Observaciones sobre la sesión")

    class Meta:
        verbose_name = "Sesión de Mesa"
        verbose_name_plural = "Sesiones de Mesa"
        ordering = ['-hora_apertura']

    def __str__(self):
        cliente_nombre = self.cliente.nombre if self.cliente else "Cliente General"
        return f"Sesión Mesa {self.mesa.numero} - {cliente_nombre} ({self.get_estado_display()})"

    def obtener_total(self):
        """Calcula el total de todas las órdenes de esta sesión"""
        from pos.models import OrdenPOS
        from django.db.models import Sum
        
        ordenes = OrdenPOS.objects.filter(sesion_mesa=self)
        total = Decimal('0.00')
        
        for orden in ordenes:
            total += orden.obtener_total()
        
        return total

    def save(self, *args, **kwargs):
        """Al guardar, actualizar el estado de la mesa"""
        is_new = self._state.adding
        
        # Si es nueva sesión activa, marcar mesa como ocupada
        if is_new and self.estado == 'activa':
            self.mesa.estado = 'ocupada'
            self.mesa.save()
        
        # Si se cierra la sesión, marcar mesa como libre
        if not is_new and self.estado in ['cerrada', 'cancelada']:
            # Verificar que no hay otras sesiones activas
            otras_activas = SesionMesa.objects.filter(
                mesa=self.mesa,
                estado='activa'
            ).exclude(pk=self.pk).exists()
            
            if not otras_activas:
                self.mesa.estado = 'libre'
                self.mesa.save()
        
        super().save(*args, **kwargs)
