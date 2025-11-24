"""Script para probar el modelo de Facturas.

Usage: python scripts/test_facturas.py
"""
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Make sure project root is on sys.path so `oddo_project` is importable
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oddo_project.settings')
django.setup()

from api.models import Factura
from decimal import Decimal

def main():
    print('Facturas antes:', Factura.objects.count())
    
    # Crear una factura de ejemplo
    factura = Factura.objects.create(
        direccion="Calle Mayor 123, Madrid, España",
        cliente="Juan Pérez",
        vendedor="María García",
        cantidad_dinero=Decimal('1250.75')
    )
    
    print(f'Factura creada: {factura}')
    print('Facturas después:', Factura.objects.count())
    
    # Mostrar todas las facturas
    print('\nTodas las facturas:')
    for f in Factura.objects.all():
        print(f'  - ID: {f.id}, Cliente: {f.cliente}, Cantidad: ${f.cantidad_dinero}, Fecha: {f.fecha_creacion.strftime("%Y-%m-%d %H:%M")}')

if __name__ == '__main__':
    main()