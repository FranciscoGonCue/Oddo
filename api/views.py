from rest_framework import viewsets
from .models import Item, Factura
from .serializers import ItemSerializer, FacturaSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created_at')
    serializer_class = ItemSerializer


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all().order_by('-fecha_creacion')
    serializer_class = FacturaSerializer
