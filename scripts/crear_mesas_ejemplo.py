#!/usr/bin/env python
"""
Script para crear mesas de ejemplo en el sistema.
Crea un layout típico de bar/restaurante con diferentes tamaños de mesas.
"""
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oddo_project.settings')
django.setup()

from mesas.models import Mesa


def crear_mesas_ejemplo():
    """Crea un layout de ejemplo con mesas de diferentes capacidades."""
    
    print("🪑 Creando mesas de ejemplo...")
    
    # Limpiar mesas existentes
    Mesa.objects.all().delete()
    
    # Layout del bar/restaurante:
    # - Mesas pequeñas (2 personas): Para parejas
    # - Mesas medianas (4 personas): Para grupos pequeños
    # - Mesas grandes (6-8 personas): Para grupos grandes
    
    layout_mesas = [
        # Fila 1 - Mesas pequeñas junto a la ventana
        {'numero': 1, 'capacidad': 2, 'posicion_x': 50, 'posicion_y': 50},
        {'numero': 2, 'capacidad': 2, 'posicion_x': 200, 'posicion_y': 50},
        {'numero': 3, 'capacidad': 2, 'posicion_x': 350, 'posicion_y': 50},
        {'numero': 4, 'capacidad': 2, 'posicion_x': 500, 'posicion_y': 50},
        
        # Fila 2 - Mesas medianas centrales
        {'numero': 5, 'capacidad': 4, 'posicion_x': 50, 'posicion_y': 200},
        {'numero': 6, 'capacidad': 4, 'posicion_x': 250, 'posicion_y': 200},
        {'numero': 7, 'capacidad': 4, 'posicion_x': 450, 'posicion_y': 200},
        
        # Fila 3 - Mesas medianas
        {'numero': 8, 'capacidad': 4, 'posicion_x': 50, 'posicion_y': 350},
        {'numero': 9, 'capacidad': 4, 'posicion_x': 250, 'posicion_y': 350},
        {'numero': 10, 'capacidad': 4, 'posicion_x': 450, 'posicion_y': 350},
        
        # Fila 4 - Mesas grandes para grupos
        {'numero': 11, 'capacidad': 6, 'posicion_x': 100, 'posicion_y': 500},
        {'numero': 12, 'capacidad': 6, 'posicion_x': 350, 'posicion_y': 500},
        
        # Mesa VIP - Grande en esquina
        {'numero': 13, 'capacidad': 8, 'posicion_x': 550, 'posicion_y': 400},
    ]
    
    mesas_creadas = []
    for datos in layout_mesas:
        mesa = Mesa.objects.create(**datos)
        mesas_creadas.append(mesa)
        print(f"  ✅ Mesa {mesa.numero} creada (capacidad: {mesa.capacidad} personas) en posición ({mesa.posicion_x}, {mesa.posicion_y})")
    
    print(f"\n✨ {len(mesas_creadas)} mesas creadas exitosamente!")
    print(f"📊 Distribución:")
    print(f"   - Mesas 2 personas: {Mesa.objects.filter(capacidad=2).count()}")
    print(f"   - Mesas 4 personas: {Mesa.objects.filter(capacidad=4).count()}")
    print(f"   - Mesas 6 personas: {Mesa.objects.filter(capacidad=6).count()}")
    print(f"   - Mesas 8 personas: {Mesa.objects.filter(capacidad=8).count()}")
    print(f"\n🌐 Accede a la interfaz gráfica en: http://0.0.0.0:8000/mesas/")
    

if __name__ == '__main__':
    crear_mesas_ejemplo()
