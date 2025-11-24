from rest_framework import serializers
from .models import Item, Factura


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_at']


class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = ['id', 'direccion', 'cliente', 'vendedor', 'fecha_creacion', 'cantidad_dinero']
        read_only_fields = ['fecha_creacion']
