from django.contrib import admin
from .models import Almacen, CantidadStock


@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'fecha_creacion']
    search_fields = ['nombre']
    readonly_fields = ['id', 'fecha_creacion']


@admin.register(CantidadStock)
class CantidadStockAdmin(admin.ModelAdmin):
    list_display = ['producto', 'ubicacion', 'cantidad', 'fecha_actualizacion']
    list_filter = ['ubicacion', 'fecha_actualizacion']
    search_fields = ['producto__nombre', 'ubicacion__nombre']
    readonly_fields = ['id', 'fecha_actualizacion']
