from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import OrdenCompra, LineaOrdenCompra
from .serializers import (
    OrdenCompraSerializer, 
    OrdenCompraCreateSerializer, 
    LineaOrdenCompraSerializer
)


class OrdenCompraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Órdenes de Compra
    
    Usa OrdenCompraCreateSerializer para POST con líneas anidadas
    """
    queryset = OrdenCompra.objects.all().order_by('-fecha_orden')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrdenCompraCreateSerializer
        return OrdenCompraSerializer
    
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        """Confirmar orden de compra"""
        orden_compra = self.get_object()
        orden_compra.estado = 'confirmado'
        orden_compra.save()
        serializer = self.get_serializer(orden_compra)
        return Response(serializer.data)


class LineaOrdenCompraViewSet(viewsets.ModelViewSet):
    """ViewSet para líneas de Órdenes de Compra"""
    queryset = LineaOrdenCompra.objects.all()
    serializer_class = LineaOrdenCompraSerializer
