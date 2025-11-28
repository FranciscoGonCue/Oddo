from rest_framework import serializers
from .models import Almacen, CantidadStock


class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = ['id', 'nombre', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']


class CantidadStockSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)
    nombre_ubicacion = serializers.CharField(source='ubicacion.nombre', read_only=True)
    
    class Meta:
        model = CantidadStock
        fields = ['id', 'producto', 'nombre_producto', 'ubicacion', 'nombre_ubicacion', 'cantidad', 'fecha_actualizacion']
        read_only_fields = ['id', 'fecha_actualizacion']
