from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import Factura, Pago, LineaFactura
from .serializers import FacturaSerializer, PagoSerializer, LineaFacturaSerializer


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
    
    @action(detail=True, methods=['get'])
    def descargar_pdf(self, request, pk=None):
        """Descargar el PDF de la factura"""
        factura = self.get_object()
        
        if not factura.pdf_file:
            return Response({'error': 'PDF no disponible'}, status=404)
        
        return FileResponse(
            factura.pdf_file.open('rb'),
            as_attachment=True,
            filename=f'factura_{factura.numero_orden}.pdf'
        )


class PagoViewSet(viewsets.ModelViewSet):
    """ViewSet para Pagos"""
    queryset = Pago.objects.all().order_by('-fecha')
    serializer_class = PagoSerializer


class LineaFacturaViewSet(viewsets.ModelViewSet):
    """ViewSet para Líneas de Factura"""
    queryset = LineaFactura.objects.all()
    serializer_class = LineaFacturaSerializer
