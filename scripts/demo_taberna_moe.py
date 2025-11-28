#!/usr/bin/env python
"""
🍺 Demo del Sistema de Gestión de la Taberna de Moe

Este script demuestra el funcionamiento completo del sistema:
1. Crear partners (clientes y proveedores)
2. Crear productos
3. Crear almacenes
4. Gestionar stock
5. Crear tickets de venta
6. Manejar fiados y facturas
7. Registrar pagos
"""

import os
import sys
import django
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oddo_project.settings')
django.setup()

from core.models import Socio, Producto
from inventory.models import Almacen, CantidadStock
from pos.models import OrdenPOS, LineaOrdenPOS
from invoicing.models import Factura, Pago
from hr.models import Empleado


def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def main():
    print_header("🍺 DEMO: SISTEMA DE GESTIÓN - TABERNA DE MOE")
    
    # Limpiar datos anteriores de la demo
    print("\n🧹 Limpiando datos anteriores...")
    LineaOrdenPOS.objects.all().delete()
    OrdenPOS.objects.all().delete()
    Pago.objects.all().delete()
    Factura.objects.all().delete()
    CantidadStock.objects.all().delete()
    Producto.objects.all().delete()
    Almacen.objects.all().delete()
    Socio.objects.all().delete()
    Empleado.objects.all().delete()
    
    # 1. CREAR PARTNERS
    print_header("📦 1. CREANDO SOCIOS")
    
    duff = Socio.objects.create(
        nombre="Cervecería Duff",
        es_proveedor=True
    )
    print(f"✅ Proveedor creado: {duff}")
    
    homer = Socio.objects.create(
        nombre="Homer Simpson",
        es_proveedor=False
    )
    print(f"✅ Cliente creado: {homer}")
    
    barney = Socio.objects.create(
        nombre="Barney Gumble",
        es_proveedor=False
    )
    print(f"✅ Cliente creado: {barney}")
    
    # 2. CREAR PRODUCTOS
    print_header("🍺 2. CREANDO PRODUCTOS")
    
    cerveza = Producto.objects.create(
        nombre="Cerveza Duff",
        precio_venta=Decimal("5.50")
    )
    print(f"✅ Producto creado: {cerveza}")
    
    nachos = Producto.objects.create(
        nombre="Nachos",
        precio_venta=Decimal("8.00")
    )
    print(f"✅ Producto creado: {nachos}")
    
    whisky = Producto.objects.create(
        nombre="Whisky Duff",
        precio_venta=Decimal("12.00")
    )
    print(f"✅ Producto creado: {whisky}")
    
    # 3. CREAR ALMACENES
    print_header("🏭 3. CREANDO ALMACENES")
    
    barra = Almacen.objects.create(nombre="Barra Principal")
    print(f"✅ Almacén creado: {barra}")
    
    trastienda = Almacen.objects.create(nombre="Trastienda")
    print(f"✅ Almacén creado: {trastienda}")
    
    # 4. CREAR STOCK INICIAL
    print_header("📦 4. CREANDO STOCK INICIAL")
    
    stock_cerveza = CantidadStock.objects.create(
        producto=cerveza,
        ubicacion=barra,
        cantidad=Decimal("100")
    )
    print(f"✅ Stock creado: {stock_cerveza}")
    
    stock_nachos = CantidadStock.objects.create(
        producto=nachos,
        ubicacion=barra,
        cantidad=Decimal("50")
    )
    print(f"✅ Stock creado: {stock_nachos}")
    
    stock_whisky = CantidadStock.objects.create(
        producto=whisky,
        ubicacion=barra,
        cantidad=Decimal("30")
    )
    print(f"✅ Stock creado: {stock_whisky}")
    
    # 5. CREAR EMPLEADOS
    print_header("👷 5. CREANDO EMPLEADOS")
    
    moe = Empleado.objects.create(
        nombre="Moe Szyslak",
        puesto="Propietario y Bartender"
    )
    print(f"✅ Empleado creado: {moe}")
    
    # 6. VENTA NORMAL - Homer paga al contado
    print_header("🖥️ 6. VENTA AL CONTADO - HOMER")
    
    ticket1 = OrdenPOS.objects.create(
        cliente=homer,
        almacen=barra,
        estado='borrador'
    )
    
    LineaOrdenPOS.objects.create(
        orden_pos=ticket1,
        producto=cerveza,
        cantidad=5,
        precio_subtotal=cerveza.precio_venta * 5
    )
    
    LineaOrdenPOS.objects.create(
        orden_pos=ticket1,
        producto=nachos,
        cantidad=2,
        precio_subtotal=nachos.precio_venta * 2
    )
    
    ticket1.estado = 'pagado'
    ticket1.save()
    
    print(f"✅ Ticket creado: POS-{str(ticket1.id)[:8]}")
    print(f"   Cliente: {ticket1.cliente.nombre}")
    print(f"   Total: ${ticket1.obtener_total()}")
    print(f"   Estado: {ticket1.get_estado_display()}")
    
    # Verificar stock
    stock_cerveza.refresh_from_db()
    stock_nachos.refresh_from_db()
    print(f"\n📊 Stock actualizado:")
    print(f"   Cerveza Duff: {stock_cerveza.cantidad} unidades")
    print(f"   Nachos: {stock_nachos.cantidad} unidades")
    
    # 7. VENTA FIADA - Barney no tiene dinero
    print_header("💳 7. VENTA FIADA - BARNEY")
    
    print(f"💰 Deuda inicial de Barney: ${barney.saldo_deuda}")
    
    ticket2 = OrdenPOS.objects.create(
        cliente=barney,
        almacen=barra,
        estado='borrador'
    )
    
    LineaOrdenPOS.objects.create(
        orden_pos=ticket2,
        producto=cerveza,
        cantidad=10,
        precio_subtotal=cerveza.precio_venta * 10
    )
    
    LineaOrdenPOS.objects.create(
        orden_pos=ticket2,
        producto=whisky,
        cantidad=3,
        precio_subtotal=whisky.precio_venta * 3
    )
    
    # Marcar como fiado (esto genera factura automáticamente)
    ticket2.estado = 'fiado'
    ticket2.save()
    
    print(f"✅ Ticket creado: POS-{str(ticket2.id)[:8]}")
    print(f"   Cliente: {ticket2.cliente.nombre}")
    print(f"   Total: ${ticket2.obtener_total()}")
    print(f"   Estado: {ticket2.get_estado_display()}")
    
    # Verificar que se creó la factura
    barney.refresh_from_db()
    facturas_barney = Factura.objects.filter(socio=barney)
    print(f"\n📄 Facturas generadas automáticamente: {facturas_barney.count()}")
    for factura in facturas_barney:
        print(f"   - INV-{str(factura.id)[:8]}: ${factura.monto_total} [{factura.get_estado_display()}]")
    
    print(f"\n💰 Deuda actualizada de Barney: ${barney.saldo_deuda}")
    
    # 8. REGISTRAR PAGO PARCIAL
    print_header("💵 8. PAGO PARCIAL DE BARNEY")
    
    factura = facturas_barney.first()
    pago_parcial = Pago.objects.create(
        factura=factura,
        monto=Decimal("50.00"),
        metodo='efectivo'
    )
    
    print(f"✅ Pago registrado: ${pago_parcial.monto} ({pago_parcial.get_metodo_display()})")
    
    barney.refresh_from_db()
    factura.refresh_from_db()
    
    print(f"💰 Deuda restante de Barney: ${barney.saldo_deuda}")
    print(f"📄 Estado de la factura: {factura.get_estado_display()}")
    
    # 9. PAGO COMPLETO
    print_header("💵 9. PAGO COMPLETO DE BARNEY")
    
    monto_restante = factura.monto_total - Decimal("50.00")
    pago_final = Pago.objects.create(
        factura=factura,
        monto=monto_restante,
        metodo='efectivo'
    )
    
    print(f"✅ Pago final registrado: ${pago_final.monto}")
    
    barney.refresh_from_db()
    factura.refresh_from_db()
    
    print(f"💰 Deuda final de Barney: ${barney.saldo_deuda}")
    print(f"📄 Estado de la factura: {factura.get_estado_display()}")
    
    # 10. RESUMEN FINAL
    print_header("📊 RESUMEN FINAL DEL SISTEMA")
    
    print("\n👥 CLIENTES:")
    for socio in Socio.objects.filter(es_proveedor=False):
        print(f"   - {socio.nombre}: Deuda ${socio.saldo_deuda}")
    
    print("\n📦 STOCK ACTUAL:")
    for stock in CantidadStock.objects.all():
        print(f"   - {stock.producto.nombre} @ {stock.ubicacion.nombre}: {stock.cantidad}")
    
    print("\n🎫 TICKETS DE VENTA:")
    for ticket in OrdenPOS.objects.all():
        print(f"   - POS-{str(ticket.id)[:8]}: {ticket.cliente.nombre} - ${ticket.obtener_total()} [{ticket.get_estado_display()}]")
    
    print("\n📄 FACTURAS:")
    for factura in Factura.objects.all():
        print(f"   - INV-{str(factura.id)[:8]}: {factura.socio.nombre} - ${factura.monto_total} [{factura.get_estado_display()}]")
    
    print("\n💵 PAGOS:")
    for pago in Pago.objects.all():
        print(f"   - ${pago.monto} ({pago.get_metodo_display()}) - Factura: INV-{str(pago.factura.id)[:8]}")
    
    print_header("✅ DEMO COMPLETADA CON ÉXITO")
    print("\n🎉 ¡El sistema funciona perfectamente!")
    print("🍺 ¡La Taberna de Moe está lista para operar!\n")


if __name__ == '__main__':
    main()
