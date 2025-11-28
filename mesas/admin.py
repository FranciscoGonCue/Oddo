from django.contrib import admin
from .models import Mesa, SesionMesa


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'capacidad', 'estado', 'forma', 'fecha_creacion']
    list_filter = ['estado', 'forma', 'capacidad']
    search_fields = ['numero']
    readonly_fields = ['id', 'fecha_creacion']
    
    fieldsets = (
        ('Información de la Mesa', {
            'fields': ('id', 'numero', 'capacidad', 'estado', 'forma')
        }),
        ('Posición en el Plano', {
            'fields': ('posicion_x', 'posicion_y'),
            'classes': ('collapse',)
        }),
        ('Información del Sistema', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SesionMesa)
class SesionMesaAdmin(admin.ModelAdmin):
    list_display = ['mesa', 'cliente', 'numero_personas', 'hora_apertura', 'hora_cierre', 'estado']
    list_filter = ['estado', 'hora_apertura']
    search_fields = ['mesa__numero', 'cliente__nombre']
    readonly_fields = ['id', 'hora_apertura']
    
    fieldsets = (
        ('Información de la Sesión', {
            'fields': ('id', 'mesa', 'cliente', 'numero_personas', 'estado')
        }),
        ('Horarios', {
            'fields': ('hora_apertura', 'hora_cierre')
        }),
        ('Observaciones', {
            'fields': ('notas',),
            'classes': ('collapse',)
        }),
    )
