from django.contrib import admin
from .models import Factura, Pago


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
    readonly_fields = ['id', 'fecha']


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['id', 'socio', 'origen', 'monto_total', 'estado', 'fecha_vencimiento', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['socio__nombre', 'origen']
    readonly_fields = ['id', 'fecha_creacion']
    inlines = [PagoInline]
    
    fieldsets = (
        ('Información de la Factura', {
            'fields': ('id', 'origen', 'socio', 'monto_total', 'estado', 'fecha_vencimiento')
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'factura', 'monto', 'metodo', 'fecha']
    list_filter = ['metodo', 'fecha']
    search_fields = ['factura__socio__nombre']
    readonly_fields = ['id', 'fecha']
