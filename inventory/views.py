from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Almacen, CantidadStock
from .serializers import AlmacenSerializer, CantidadStockSerializer


class AlmacenViewSet(viewsets.ModelViewSet):
    """ViewSet para Almacenes"""
    queryset = Almacen.objects.all().order_by('nombre')
    serializer_class = AlmacenSerializer
    
    @action(detail=True, methods=['get'])
    def inventario(self, request, pk=None):
        """Ver inventario completo de un almacén"""
        almacen = self.get_object()
        cantidades_stock = almacen.cantidades_stock.all()
        serializer = CantidadStockSerializer(cantidades_stock, many=True)
        return Response(serializer.data)


class CantidadStockViewSet(viewsets.ModelViewSet):
    """ViewSet para Cantidades de Stock"""
    queryset = CantidadStock.objects.all().order_by('producto__nombre')
    serializer_class = CantidadStockSerializer
