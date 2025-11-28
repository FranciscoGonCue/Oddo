from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import OrdenPOS, LineaOrdenPOS
from .serializers import OrdenPOSSerializer, OrdenPOSCreateSerializer, LineaOrdenPOSSerializer


class OrdenPOSViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Órdenes POS (Tickets)
    
    Usa OrdenPOSCreateSerializer para POST con líneas anidadas
    """
    queryset = OrdenPOS.objects.all().order_by('-fecha')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrdenPOSCreateSerializer
        return OrdenPOSSerializer
    
    @action(detail=True, methods=['post'])
    def marcar_pagado(self, request, pk=None):
        """Marcar ticket como pagado"""
        orden_pos = self.get_object()
        orden_pos.estado = 'pagado'
        orden_pos.save()
        serializer = self.get_serializer(orden_pos)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def marcar_fiado(self, request, pk=None):
        """Marcar ticket como fiado (genera factura automáticamente)"""
        orden_pos = self.get_object()
        if not orden_pos.cliente:
            return Response(
                {'error': 'No se puede fiar sin un cliente asignado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        orden_pos.estado = 'fiado'
        orden_pos.save()
        serializer = self.get_serializer(orden_pos)
        return Response(serializer.data)


class LineaOrdenPOSViewSet(viewsets.ModelViewSet):
    """ViewSet para líneas de Órdenes POS"""
    queryset = LineaOrdenPOS.objects.all()
    serializer_class = LineaOrdenPOSSerializer
