from django.contrib import admin
from .models import Socio, Producto


@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'es_proveedor', 'saldo_deuda', 'fecha_creacion']
    list_filter = ['es_proveedor', 'fecha_creacion']
    search_fields = ['nombre']
    readonly_fields = ['id', 'fecha_creacion', 'saldo_deuda']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id', 'nombre', 'es_proveedor')
        }),
        ('Información Financiera', {
            'fields': ('saldo_deuda',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio_venta', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['nombre']
    readonly_fields = ['id', 'fecha_creacion']
