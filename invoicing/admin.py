from django.contrib import admin
from .models import Factura, Pago, LineaFactura, ConfiguracionEmpresa


class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1
    readonly_fields = ['id', 'importe']
    fields = ['producto', 'codigo_producto', 'descripcion', 'cantidad', 'precio_unitario', 'tasa_impuesto', 'importe']


class PagoInline(admin.TabularInline):
    model = Pago
    extra = 1
    readonly_fields = ['id', 'fecha']


@admin.register(ConfiguracionEmpresa)
class ConfiguracionEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion_linea1']
    
    fieldsets = (
        ('Datos de la Empresa', {
            'fields': ('nombre', 'direccion_linea1', 'direccion_linea2', 'direccion_linea3', 'direccion_linea4', 'logo')
        }),
        ('Dirección de Facturación', {
            'fields': ('direccion_facturacion_nombre', 'direccion_facturacion_linea1', 
                      'direccion_facturacion_linea2', 'direccion_facturacion_linea3', 'telefono_facturacion')
        }),
    )


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_orden', 'socio', 'cliente_nombre', 'vendedor', 'monto_total', 'estado', 'fecha_creacion', 'tiene_pdf']
    list_filter = ['estado', 'fecha_creacion', 'fecha_vencimiento']
    search_fields = ['numero_orden', 'socio__nombre', 'cliente_nombre', 'origen']
    readonly_fields = ['id', 'numero_orden', 'fecha_creacion', 'pdf_file']
    inlines = [LineaFacturaInline, PagoInline]
    
    fieldsets = (
        ('Información de la Factura', {
            'fields': ('id', 'numero_orden', 'origen', 'socio', 'vendedor', 'estado', 'fecha_vencimiento')
        }),
        ('Datos del Cliente', {
            'fields': ('cliente_nombre', 'cliente_direccion', 'cliente_ciudad', 'cliente_identificacion')
        }),
        ('Montos e Impuestos', {
            'fields': ('monto_total', 'tasa_impuesto')
        }),
        ('PDF Generado', {
            'fields': ('pdf_file',),
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )
    
    def tiene_pdf(self, obj):
        return bool(obj.pdf_file)
    tiene_pdf.boolean = True
    tiene_pdf.short_description = 'PDF'


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id', 'factura', 'monto', 'metodo', 'fecha']
    list_filter = ['metodo', 'fecha']
    search_fields = ['factura__socio__nombre', 'factura__numero_orden']
    readonly_fields = ['id', 'fecha']


@admin.register(LineaFactura)
class LineaFacturaAdmin(admin.ModelAdmin):
    list_display = ['factura', 'descripcion', 'cantidad', 'precio_unitario', 'importe']
    list_filter = ['factura']
    search_fields = ['descripcion', 'codigo_producto', 'factura__numero_orden']
    readonly_fields = ['id', 'importe']
