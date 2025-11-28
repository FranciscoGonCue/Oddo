from django.contrib import admin
from .models import Empleado


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'puesto', 'fecha_creacion']
    list_filter = ['puesto', 'fecha_creacion']
    search_fields = ['nombre', 'puesto']
    readonly_fields = ['id', 'fecha_creacion']
