from django.contrib import admin
from .models import Item, Factura


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'vendedor', 'cantidad_dinero', 'fecha_creacion']
    list_filter = ['fecha_creacion', 'vendedor']
    search_fields = ['cliente', 'vendedor', 'direccion']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información de la Factura', {
            'fields': ('cliente', 'vendedor', 'direccion')
        }),
        ('Detalles Financieros', {
            'fields': ('cantidad_dinero',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )