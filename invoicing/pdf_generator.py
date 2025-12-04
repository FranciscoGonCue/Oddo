"""
Generador de PDFs para facturas
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from django.conf import settings
from decimal import Decimal
import os
from io import BytesIO


def generar_pdf_factura(factura):
    """
    Genera un PDF para una factura siguiendo el formato proporcionado
    
    Args:
        factura: Instancia del modelo Factura
        
    Returns:
        BytesIO: Buffer con el PDF generado
    """
    buffer = BytesIO()
    
    # Crear el documento
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )
    
    # Contenedor de elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    style_normal = styles['Normal']
    style_heading = styles['Heading1']
    
    # Estilo personalizado para encabezados pequeños
    style_small = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#666666')
    )
    
    style_bold = ParagraphStyle(
        'Bold',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold'
    )
    
    # Obtener configuración de empresa
    from .models import ConfiguracionEmpresa
    config = ConfiguracionEmpresa.get_config()
    
    # =============================================================================
    # SECCIÓN 1: Logo y datos de la empresa
    # =============================================================================
    logo_text = Paragraph("<b>📸 Your logo</b>", style_normal)
    
    empresa_data = [
        [logo_text, ''],
    ]
    
    empresa_info = f"""
    <b>{config.nombre}</b><br/>
    {config.direccion_linea1}<br/>
    {config.direccion_linea2}<br/>
    {config.direccion_linea3}<br/>
    {config.direccion_linea4}
    """
    
    empresa_data.append([Paragraph(empresa_info, style_small), ''])
    
    empresa_table = Table(empresa_data, colWidths=[3.5*inch, 3*inch])
    empresa_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(empresa_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # =============================================================================
    # SECCIÓN 2: Dirección de facturación y datos del cliente
    # =============================================================================
    facturacion_info = f"""
    <b>Dirección de facturación y envío</b><br/>
    {config.direccion_facturacion_nombre}<br/>
    {config.direccion_facturacion_linea1}<br/>
    {config.direccion_facturacion_linea2}<br/>
    {config.direccion_facturacion_linea3}<br/>
    ☎ {config.telefono_facturacion}
    """
    
    cliente_info = f"""
    <b>{factura.cliente_nombre}</b><br/>
    {factura.cliente_direccion}<br/>
    {factura.cliente_ciudad}<br/>
    {factura.cliente_identificacion}
    """
    
    direcciones_data = [
        [Paragraph(facturacion_info, style_small), Paragraph(cliente_info, style_small)]
    ]
    
    direcciones_table = Table(direcciones_data, colWidths=[3.5*inch, 3*inch])
    direcciones_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    elements.append(direcciones_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # =============================================================================
    # SECCIÓN 3: Número de orden
    # =============================================================================
    orden_title = Paragraph(f"<b>Número de orden {factura.numero_orden}</b>", style_heading)
    elements.append(orden_title)
    elements.append(Spacer(1, 0.2*inch))
    
    # =============================================================================
    # SECCIÓN 4: Fecha y Vendedor
    # =============================================================================
    fecha_vendedor_data = [
        ['Fecha de la orden', 'Vendedor'],
        [factura.fecha_creacion.strftime('%d/%m/%Y'), factura.vendedor]
    ]
    
    fecha_vendedor_table = Table(fecha_vendedor_data, colWidths=[3.5*inch, 3*inch])
    fecha_vendedor_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
    ]))
    
    elements.append(fecha_vendedor_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # =============================================================================
    # SECCIÓN 5: Tabla de productos
    # =============================================================================
    # Encabezados de la tabla
    tabla_data = [
        ['Descripción', 'Cantidad', 'Precio unitario', 'Impuestos', 'Importe']
    ]
    
    # Agregar líneas de la factura
    for linea in factura.lineas.all():
        codigo = f"[{linea.codigo_producto}] " if linea.codigo_producto else ""
        descripcion = f"{codigo}{linea.descripcion}"
        
        cantidad_texto = f"{linea.cantidad:.2f} Unidades"
        precio_texto = f"${linea.precio_unitario:,.2f}"
        impuesto_texto = f"{linea.tasa_impuesto:.0f}% Exportaciones"
        importe_texto = f"${linea.importe:,.2f}"
        
        tabla_data.append([
            descripcion,
            cantidad_texto,
            precio_texto,
            impuesto_texto,
            importe_texto
        ])
    
    # Crear tabla de productos
    productos_table = Table(tabla_data, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1.2*inch, 1*inch])
    productos_table.setStyle(TableStyle([
        # Encabezados
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Contenido
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
        ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
        
        # Líneas
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.grey),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.grey),
        
        # Padding
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
    ]))
    
    elements.append(productos_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # =============================================================================
    # SECCIÓN 6: Totales
    # =============================================================================
    # Calcular subtotal e impuestos
    subtotal = sum(linea.importe for linea in factura.lineas.all())
    impuesto_total = subtotal * (factura.tasa_impuesto / Decimal('100'))
    total = subtotal + impuesto_total
    
    totales_data = [
        ['', 'Subtotal', f'${subtotal:,.2f}'],
        ['', f'Impuesto del {factura.tasa_impuesto:.0f}%', f'${impuesto_total:,.2f}'],
        ['', 'Total', f'${total:,.2f}'],
    ]
    
    totales_table = Table(totales_data, colWidths=[4*inch, 1.5*inch, 1.5*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 0), (2, -1), 'Helvetica'),
        ('FONTSIZE', (1, 0), (-1, -1), 10),
        ('LINEABOVE', (1, -1), (-1, -1), 1.5, colors.black),
        ('TOPPADDING', (1, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
    ]))
    
    elements.append(totales_table)
    
    # Construir el PDF
    doc.build(elements)
    
    # Resetear el buffer al inicio
    buffer.seek(0)
    return buffer
