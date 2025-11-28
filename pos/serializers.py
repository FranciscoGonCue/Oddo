from rest_framework import serializers
from .models import OrdenPOS, LineaOrdenPOS


class LineaOrdenPOSSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='producto.nombre', read_only=True)
    
    class Meta:
        model = LineaOrdenPOS
        fields = ['id', 'producto', 'nombre_producto', 'cantidad', 'precio_subtotal']
        read_only_fields = ['id']


class OrdenPOSSerializer(serializers.ModelSerializer):
    nombre_cliente = serializers.CharField(source='cliente.nombre', read_only=True, allow_null=True)
    nombre_almacen = serializers.CharField(source='almacen.nombre', read_only=True, allow_null=True)
    lineas = LineaOrdenPOSSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrdenPOS
        fields = ['id', 'id_sesion', 'cliente', 'nombre_cliente', 'almacen', 'nombre_almacen', 
                  'fecha', 'estado', 'metodo_pago', 'lineas', 'total']
        read_only_fields = ['id', 'fecha']
    
    def get_total(self, obj):
        return str(obj.obtener_total())


class OrdenPOSCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear tickets con líneas anidadas"""
    lineas = LineaOrdenPOSSerializer(many=True)
    
    class Meta:
        model = OrdenPOS
        fields = ['id', 'id_sesion', 'sesion_mesa', 'cliente', 'almacen', 'estado', 'lineas']
        read_only_fields = ['id']
    
    def create(self, validated_data):
        lineas_data = validated_data.pop('lineas')
        orden_pos = OrdenPOS.objects.create(**validated_data)
        for linea_data in lineas_data:
            # Si no se proporciona precio_subtotal, se calculará automáticamente en el save()
            LineaOrdenPOS.objects.create(orden_pos=orden_pos, **linea_data)
        return orden_pos
