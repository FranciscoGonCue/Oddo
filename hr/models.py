from django.db import models
import uuid


# =============================================================================
# 👷 MÓDULO EMPLEADOS (HR)
# =============================================================================

class Empleado(models.Model):
    """Personal de la taberna"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=200, help_text="Nombre del empleado")
    puesto = models.CharField(max_length=100, help_text="Cargo/Puesto")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        ordering = ['nombre']

    def __str__(self):
        return f"👷 {self.nombre} - {self.puesto}"
