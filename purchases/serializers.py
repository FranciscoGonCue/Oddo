from rest_framework import serializers
from .models import OrdenCompra, LineaOrdenCompra


class LineaOrdenCompraSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = LineaOrdenCompra
        fields = ['id', 'producto', 'nombre_producto', 'cantidad']
        read_only_fields = ['id']


class OrdenCompraSerializer(serializers.ModelSerializer):
    nombre_proveedor = serializers.CharField(source='proveedor.nombre', read_only=True)
    lineas = LineaOrdenCompraSerializer(many=True, read_only=True)
    
    class Meta:
        model = OrdenCompra
        fields = ['id', 'proveedor', 'nombre_proveedor', 'fecha_orden', 'estado', 'lineas']
        read_only_fields = ['id', 'fecha_orden']


class OrdenCompraCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear órdenes de compra con líneas anidadas"""
    lineas = LineaOrdenCompraSerializer(many=True)
    
    class Meta:
        model = OrdenCompra
        fields = ['id', 'proveedor', 'estado', 'lineas']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        lineas_data = validated_data.pop('lineas')
        orden_compra = OrdenCompra.objects.create(**validated_data)
        for linea_data in lineas_data:
            LineaOrdenCompra.objects.create(orden_compra=orden_compra, **linea_data)
        return orden_compra
