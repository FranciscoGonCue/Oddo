from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Socio, Producto
from .serializers import SocioSerializer, ProductoSerializer


class SocioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Socios (Clientes y Proveedores)
    
    Acciones adicionales:
    - GET /api/socios/proveedores/ - Lista solo proveedores
    - GET /api/socios/clientes/ - Lista solo clientes
    """
    queryset = Socio.objects.all().order_by('nombre')
    serializer_class = SocioSerializer
    
    @action(detail=False, methods=['get'])
    def proveedores(self, request):
        """Listar solo proveedores"""
        proveedores = Socio.objects.filter(es_proveedor=True)
        serializer = self.get_serializer(proveedores, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def clientes(self, request):
        """Listar solo clientes"""
        clientes = Socio.objects.filter(es_proveedor=False)
        serializer = self.get_serializer(clientes, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def historial_deudas(self, request, pk=None):
        """Ver historial de deudas y facturas de un socio"""
        from invoicing.serializers import FacturaSerializer
        socio = self.get_object()
        facturas = socio.facturas.all()
        factura_serializer = FacturaSerializer(facturas, many=True)
        return Response({
            'socio': SocioSerializer(socio).data,
            'facturas': factura_serializer.data
        })


class ProductoViewSet(viewsets.ModelViewSet):
    """ViewSet para Productos (Bebidas y comida)"""
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    
    @action(detail=True, methods=['get'])
    def stock(self, request, pk=None):
        """Ver stock del producto en todos los almacenes"""
        from inventory.serializers import CantidadStockSerializer
        producto = self.get_object()
        cantidades_stock = producto.cantidades_stock.all()
        serializer = CantidadStockSerializer(cantidades_stock, many=True)
        return Response(serializer.data)
