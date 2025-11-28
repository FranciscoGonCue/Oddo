from django.contrib import admin
from .models import OrdenPOS, LineaOrdenPOS


class LineaOrdenPOSInline(admin.TabularInline):
    model = LineaOrdenPOS
    extra = 1
    readonly_fields = ['id', 'precio_subtotal']


@admin.register(OrdenPOS)
class OrdenPOSAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'almacen', 'fecha', 'estado', 'obtener_total']
    list_filter = ['estado', 'fecha', 'almacen']
    search_fields = ['cliente__nombre', 'id_sesion']
    readonly_fields = ['id', 'fecha']
    inlines = [LineaOrdenPOSInline]
    
    fieldsets = (
        ('Información del Ticket', {
            'fields': ('id', 'id_sesion', 'cliente', 'almacen', 'estado')
        }),
        ('Información del Sistema', {
            'fields': ('fecha',),
            'classes': ('collapse',)
        }),
    )
    
    def obtener_total(self, obj):
        return f"${obj.obtener_total()}"
    obtener_total.short_description = 'Total'


@admin.register(LineaOrdenPOS)
class LineaOrdenPOSAdmin(admin.ModelAdmin):
    list_display = ['id', 'orden_pos', 'producto', 'cantidad', 'precio_subtotal']
    search_fields = ['producto__nombre', 'orden_pos__cliente__nombre']
    readonly_fields = ['id']
