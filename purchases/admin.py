from django.contrib import admin
from .models import OrdenCompra, LineaOrdenCompra


class LineaOrdenCompraInline(admin.TabularInline):
    model = LineaOrdenCompra
    extra = 1
    readonly_fields = ['id']


@admin.register(OrdenCompra)
class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'proveedor', 'fecha_orden', 'estado']
    list_filter = ['estado', 'fecha_orden']
    search_fields = ['proveedor__nombre']
    readonly_fields = ['id', 'fecha_orden']
    inlines = [LineaOrdenCompraInline]
    
    fieldsets = (
        ('Información del Pedido', {
            'fields': ('id', 'proveedor', 'estado')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_orden',),
            'classes': ('collapse',)
        }),
    )


@admin.register(LineaOrdenCompra)
class LineaOrdenCompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'orden_compra', 'producto', 'cantidad']
    list_filter = ['orden_compra__estado']
    search_fields = ['producto__nombre', 'orden_compra__proveedor__nombre']
    readonly_fields = ['id']
