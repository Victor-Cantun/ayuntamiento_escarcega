import os
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime
from io import BytesIO

def generate_pdf_receipt(payment):
    """Genera un PDF del recibo de pago"""
    try:
        # Crear buffer en memoria
        buffer = BytesIO()
        
        # Crear documento
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para el título
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.darkblue,
            alignment=1,  # Centrado
        )
        
        # Título
        story.append(Paragraph("RECIBO DE COMPRA", title_style))
        story.append(Spacer(1, 20))
        
        # Información del recibo
        info_data = [
            ['Número de Factura:', payment.invoice_number],
            ['Fecha:', payment.created_at.strftime('%d/%m/%Y %H:%M')],
            ['Cliente:', payment.user.get_full_name() or payment.user.username],
            ['Email:', payment.customer_email],
            ['Estado:', payment.get_status_display()],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Tabla de productos
        story.append(Paragraph("PRODUCTOS COMPRADOS", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Encabezados de la tabla
        products_data = [['Producto', 'Cantidad', 'Precio Unitario', 'Total']]
        
        # Agregar productos
        for item in payment.items.all():
            products_data.append([
                item.product.name,
                str(item.quantity),
                f"${item.unit_price:.2f}",
                f"${item.total_price:.2f}"
            ])
        
        # Fila de total
        products_data.append(['', '', 'TOTAL:', f"${payment.total_amount:.2f}"])
        
        products_table = Table(products_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        products_table.setStyle(TableStyle([
            # Encabezado
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            
            # Datos
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('GRID', (0, 0), (-1, -2), 1, colors.black),
            
            # Total
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ]))
        
        story.append(products_table)
        story.append(Spacer(1, 30))
        
        # Pie de página
        footer_text = """
        <para align=center>
        <b>¡Gracias por tu compra!</b><br/>
        Si tienes alguna pregunta, contáctanos en soporte@tutienda.com<br/>
        <i>Este es un recibo generado automáticamente.</i>
        </para>
        """
        story.append(Paragraph(footer_text, styles['Normal']))
        
        # Construir PDF
        doc.build(story)
        
        # Guardar archivo
        buffer.seek(0)
        filename = f"recibo_{payment.invoice_number}.pdf"
        
        # Crear directorio si no existe
        receipts_dir = os.path.join(settings.MEDIA_ROOT, 'receipts')
        os.makedirs(receipts_dir, exist_ok=True)
        
        file_path = os.path.join(receipts_dir, filename)
        
        # Guardar el archivo
        with open(file_path, 'wb') as f:
            f.write(buffer.getvalue())
        
        # Actualizar el campo del modelo
        payment.pdf_receipt.save(filename, ContentFile(buffer.getvalue()))
        
        return file_path
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return None