from rest_framework import serializers
from .models import Empleado


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ['id', 'nombre', 'puesto', 'fecha_creacion']
        read_only_fields = ['id', 'fecha_creacion']
