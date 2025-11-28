from rest_framework import serializers
from .models import Mesa, SesionMesa


class MesaSerializer(serializers.ModelSerializer):
    total_cuenta = serializers.SerializerMethodField()
    sesion_actual = serializers.SerializerMethodField()
    
    class Meta:
        model = Mesa
        fields = ['id', 'numero', 'capacidad', 'estado', 'posicion_x', 'posicion_y', 
                  'forma', 'fecha_creacion', 'total_cuenta', 'sesion_actual']
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_total_cuenta(self, obj):
        return str(obj.obtener_total_cuenta())
    
    def get_sesion_actual(self, obj):
        sesion = obj.obtener_sesion_actual()
        if sesion:
            return {
                'id': str(sesion.id),
                'numero_personas': sesion.numero_personas,
                'hora_apertura': sesion.hora_apertura,
                'cliente': str(sesion.cliente.id) if sesion.cliente else None,
                'nombre_cliente': sesion.cliente.nombre if sesion.cliente else None
            }
        return None


class SesionMesaSerializer(serializers.ModelSerializer):
    nombre_mesa = serializers.CharField(source='mesa.numero', read_only=True)
    nombre_cliente = serializers.CharField(source='cliente.nombre', read_only=True, allow_null=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = SesionMesa
        fields = ['id', 'mesa', 'nombre_mesa', 'cliente', 'nombre_cliente', 
                  'numero_personas', 'hora_apertura', 'hora_cierre', 'estado', 
                  'notas', 'total']
        read_only_fields = ['id', 'hora_apertura']
    
    def get_total(self, obj):
        return str(obj.obtener_total())


class SesionMesaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear sesiones de mesa"""
    
    class Meta:
        model = SesionMesa
        fields = ['id', 'mesa', 'cliente', 'numero_personas', 'estado', 'notas']
        read_only_fields = ['id']
