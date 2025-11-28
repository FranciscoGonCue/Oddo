from rest_framework import serializers
from .models import Socio, Producto


class SocioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Socio
        fields = ['id', 'nombre', 'es_proveedor', 'saldo_deuda', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion', 'saldo_deuda']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio_venta', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
