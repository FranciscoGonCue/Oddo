from rest_framework import viewsets
from .models import Empleado
from .serializers import EmpleadoSerializer


class EmpleadoViewSet(viewsets.ModelViewSet):
    """ViewSet para Empleados"""
    queryset = Empleado.objects.all().order_by('nombre')
    serializer_class = EmpleadoSerializer
