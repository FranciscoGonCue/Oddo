from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal
from .models import Factura, Pago


class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = ['id', 'factura', 'monto', 'metodo', 'fecha']
        read_only_fields = ['id', 'fecha']


class FacturaSerializer(serializers.ModelSerializer):
    nombre_socio = serializers.CharField(source='socio.nombre', read_only=True)
    pagos = PagoSerializer(many=True, read_only=True)
    total_pagado = serializers.SerializerMethodField()
    restante = serializers.SerializerMethodField()
    
    class Meta:
        model = Factura
        fields = ['id', 'origen', 'socio', 'nombre_socio', 'monto_total', 'estado', 
                  'fecha_vencimiento', 'fecha_creacion', 'pagos', 'total_pagado', 'restante']
        read_only_fields = ['id', 'fecha_creacion']
    
    def get_total_pagado(self, obj):
        total = obj.pagos.aggregate(total=Sum('monto'))['total']
        return str(total or Decimal('0.00'))
    
    def get_restante(self, obj):
        total_pagado = obj.pagos.aggregate(total=Sum('monto'))['total'] or Decimal('0.00')
        restante = obj.monto_total - total_pagado
        return str(restante)
