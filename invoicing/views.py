from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Factura, Pago
from .serializers import FacturaSerializer, PagoSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    """ViewSet para Facturas"""
    queryset = Factura.objects.all().order_by('-fecha_creacion')
    serializer_class = FacturaSerializer
    
    @action(detail=False, methods=['get'])
    def facturas_abiertas(self, request):
        """Listar facturas abiertas (pendientes de pago)"""
        facturas_abiertas = Factura.objects.filter(estado='abierto')
        serializer = self.get_serializer(facturas_abiertas, many=True)
        return Response(serializer.data)


class PagoViewSet(viewsets.ModelViewSet):
    """ViewSet para Pagos"""
    queryset = Pago.objects.all().order_by('-fecha')
    serializer_class = PagoSerializer
