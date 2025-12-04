from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import render
from .models import Mesa, SesionMesa
from .serializers import MesaSerializer, SesionMesaSerializer, SesionMesaCreateSerializer


def index(request):
    """Vista principal del plano de mesas"""
    return render(request, 'mesas/index.html')


class MesaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para Mesas
    
    Acciones adicionales:
    - POST /mesas/<id>/abrir/ - Abrir mesa (crear sesión)
    - POST /mesas/<id>/cerrar/ - Cerrar mesa (cerrar sesión activa)
    - GET /mesas/libres/ - Listar mesas libres
    - GET /mesas/ocupadas/ - Listar mesas ocupadas
    """
    queryset = Mesa.objects.all().order_by('numero')
    serializer_class = MesaSerializer
    
    @action(detail=False, methods=['get'])
    def libres(self, request):
        """Listar mesas libres"""
        mesas = Mesa.objects.filter(estado='libre')
        serializer = self.get_serializer(mesas, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def ocupadas(self, request):
        """Listar mesas ocupadas"""
        mesas = Mesa.objects.filter(estado='ocupada')
        serializer = self.get_serializer(mesas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def abrir(self, request, pk=None):
        """Abrir una mesa (crear sesión)"""
        mesa = self.get_object()
        
        if mesa.estado == 'ocupada':
            return Response(
                {'error': 'La mesa ya está ocupada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear sesión
        numero_personas = request.data.get('numero_personas', 1)
        cliente = request.data.get('cliente')
        notas = request.data.get('notas', '')
        
        sesion_data = {
            'mesa': mesa.id,
            'numero_personas': numero_personas,
            'notas': notas
        }
        
        if cliente:
            sesion_data['cliente'] = cliente
        
        sesion_serializer = SesionMesaCreateSerializer(data=sesion_data)
        if sesion_serializer.is_valid():
            sesion = sesion_serializer.save()
            mesa_serializer = self.get_serializer(mesa)
            return Response({
                'mesa': mesa_serializer.data,
                'sesion': SesionMesaSerializer(sesion).data
            })
        
        return Response(sesion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cerrar(self, request, pk=None):
        """Cerrar mesa (cerrar sesión activa y procesar pago)"""
        mesa = self.get_object()
        sesion = mesa.obtener_sesion_actual()
        
        if not sesion:
            return Response(
                {'error': 'La mesa no tiene sesión activa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener método de pago
        metodo_pago = request.data.get('metodo_pago', 'efectivo')
        
        if metodo_pago not in ['efectivo', 'tarjeta', 'transferencia']:
            return Response(
                {'error': 'Método de pago inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Procesar todas las órdenes de la sesión
        from pos.models import OrdenPOS
        from invoicing.models import Factura
        from decimal import Decimal
        
        ordenes = OrdenPOS.objects.filter(sesion_mesa=sesion, estado='borrador')
        
        if ordenes.count() == 0:
            return Response(
                {'error': 'No hay órdenes para procesar'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calcular total
        total = Decimal('0.00')
        for orden in ordenes:
            total += orden.obtener_total()
            orden.estado = 'pagado'
            orden.metodo_pago = metodo_pago
            orden.save()
        
        # Generar factura con PDF si hay cliente
        factura = None
        if sesion.cliente and total > 0:
            from invoicing.models import Factura, Pago, LineaFactura
            from django.core.files.base import ContentFile
            
            # Crear la factura
            factura = Factura.objects.create(
                origen=f"Mesa {mesa.numero} - Sesión {str(sesion.id)[:8]}",
                socio=sesion.cliente,
                vendedor=request.user.username if request.user.is_authenticated else "Sistema",
                cliente_nombre=sesion.cliente.nombre,
                monto_total=total,
                tasa_impuesto=Decimal('0.00'),
                estado='pagado'
            )
            
            # Crear líneas de factura desde las órdenes POS
            for orden in ordenes:
                for linea_orden in orden.lineas.all():
                    LineaFactura.objects.create(
                        factura=factura,
                        producto=linea_orden.producto,
                        codigo_producto=f"PROD-{linea_orden.producto.id}" if linea_orden.producto else "",
                        descripcion=linea_orden.producto.nombre if linea_orden.producto else "Producto",
                        cantidad=linea_orden.cantidad,
                        precio_unitario=linea_orden.precio_unitario,
                        tasa_impuesto=Decimal('0.00')
                    )
            
            # Generar el PDF automáticamente
            try:
                from invoicing.pdf_generator import generar_pdf_factura
                pdf_buffer = generar_pdf_factura(factura)
                pdf_filename = f'factura_{factura.numero_orden}.pdf'
                factura.pdf_file.save(pdf_filename, ContentFile(pdf_buffer.read()), save=True)
            except Exception as e:
                # Si falla el PDF, lo registramos pero no detenemos el proceso
                print(f"Error generando PDF para factura {factura.numero_orden}: {e}")
            
            # Crear el pago asociado
            Pago.objects.create(
                factura=factura,
                monto=total,
                metodo=metodo_pago
            )
        
        # Cerrar sesión
        sesion.estado = 'cerrada'
        sesion.hora_cierre = timezone.now()
        sesion.save()
        
        serializer = self.get_serializer(mesa)
        response_data = {
            'mesa': serializer.data,
            'ordenes_procesadas': ordenes.count(),
            'metodo_pago': metodo_pago,
            'total': str(total)
        }
        
        if factura:
            response_data['factura_id'] = str(factura.id)
            response_data['factura_numero'] = factura.numero_orden
            response_data['pdf_url'] = factura.pdf_file.url if factura.pdf_file else None
        
        return Response(response_data)
    
    @action(detail=True, methods=['get'])
    def cuenta(self, request, pk=None):
        """Ver cuenta actual de la mesa"""
        mesa = self.get_object()
        sesion = mesa.obtener_sesion_actual()
        
        if not sesion:
            return Response(
                {'error': 'La mesa no tiene sesión activa'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from pos.models import OrdenPOS
        from pos.serializers import OrdenPOSSerializer
        
        ordenes = OrdenPOS.objects.filter(sesion_mesa=sesion)
        ordenes_serializer = OrdenPOSSerializer(ordenes, many=True)
        
        return Response({
            'sesion': SesionMesaSerializer(sesion).data,
            'ordenes': ordenes_serializer.data,
            'total': str(sesion.obtener_total())
        })


class SesionMesaViewSet(viewsets.ModelViewSet):
    """ViewSet para Sesiones de Mesa"""
    queryset = SesionMesa.objects.all().order_by('-hora_apertura')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return SesionMesaCreateSerializer
        return SesionMesaSerializer
    
    @action(detail=False, methods=['get'])
    def activas(self, request):
        """Listar sesiones activas"""
        sesiones = SesionMesa.objects.filter(estado='activa')
        serializer = self.get_serializer(sesiones, many=True)
        return Response(serializer.data)
