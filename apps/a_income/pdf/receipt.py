import io
from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle)
from decimal import ROUND_HALF_UP
from reportlab.lib.enums import TA_RIGHT
from django.http import HttpResponse
from decimal import Decimal
#from reportlab.lib.styles import ParagraphStyle
#from django.utils import timezone
#from reportlab.lib.units import inch
#from functools import partial
#import qrcode
#from django.core.mail import EmailMessage
#from django.http import FileResponse
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from django.http import Http404

def draw_footer(c, doc):
    """
    Dibuja un pie de página en cada página.
    """
    width, height = A4
    c.saveState()
    c.setFont("Helvetica", 9)
    # 👇 Aquí cambias el título que se verá en la pestaña del navegador
    c.setTitle("Recibo de pago")
    # Texto de contacto (ajústalo a tu empresa)
    contacto = "Email: tesoreria@escarcega.gob.mx | Web: www.escarcega.gob.mx | Tel: +52 55 1234 5678"
    # Ubicación: margen inferior
    x = width / 2
    y = 15  # 15 puntos desde el borde inferior
    # Dibujar centrado
    c.drawCentredString(x, y, contacto)
    c.restoreState()

def money(value):
    q = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return f"{q:,.2f}"

def generate_payment_receipt_pdf(request, receipt,customer,items, download=False):
    #try:
    #    factura = Receipt.objects.get(pk=receipt_id)
    #except Receipt.DoesNotExist:
    #    raise Http404("Factura no encontrada")

    #cliente = factura.customer
    #items = factura.items.all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=18*mm, leftMargin=18*mm,
                            topMargin=18*mm, bottomMargin=18*mm)

    styles = getSampleStyleSheet()
    #styleN = styles['Normal']
    styleH = styles['Heading2']
    #styleRight = ParagraphStyle(name='right', parent=styleN, alignment=2)

    flow = []

    # Logo
    logo_path = finders.find('images/logo-2.png')
    if logo_path:
        img = Image(logo_path, width=25*mm, height=25*mm)
        img.hAlign = "CENTER"  # alineado al centro
        #flow.append(img)
    else:
        flow.append(Paragraph("H. Ayuntamiento de Escárcega 2024-2027", styleH))

    #flow.append(Spacer(1, 6))

    # --- Datos de ejemplo (normalmente vienen de tus modelos)
    empresa = {
        "nombre": "H. Ayuntamiento de Escárceega",
        "rfc": "EMP123456789",
        "direccion": "Col. Centro, Escárcega, Campeche",
        "telefono": "+52 55 1234 5678",
        "email": "tesoreria@escarcega.com",
    }

    cliente = {
        "nombre": customer.get_full_name(),
        "direccion": customer.get_direction(),
        "email": customer.email,
    }

    factura = {
        "folio": receipt.id,
        "fecha": receipt.issue_date.strftime("%d/%m/%Y"),
    }

    # --- Bloque izquierdo: datos de empresa + factura
    emisor_data = [
        [Paragraph(f"<b>{empresa['nombre']}</b>", styles["Normal"])],
        [Paragraph(f"RFC: {empresa['rfc']}", styles["Normal"])],
        [Paragraph(empresa["direccion"], styles["Normal"])],
        [Paragraph(f"Tel: {empresa['telefono']}", styles["Normal"])],
        [Paragraph(f"Email: {empresa['email']}", styles["Normal"])],
        [Spacer(1, 5)],
        [Paragraph(f"<b>Factura: {factura['folio']}</b>", styles["Normal"])],
        [Paragraph(f"Fecha: {factura['fecha']}", styles["Normal"])],
    ]

    # --- Bloque derecho: datos del cliente
    cliente_data = [
        [Paragraph("<b>Cliente:</b>", styles["Normal"])],
        [Paragraph(cliente["nombre"], styles["Normal"])],
        [Paragraph(cliente["direccion"], styles["Normal"])],
        [Paragraph(cliente["email"], styles["Normal"])],
    ]

    # --- Construimos la tabla de dos columnas
    header_table = Table(
        [
            [emisor_data, cliente_data]  # una fila con dos columnas
        ],
        colWidths=[250, 250],  # ancho de cada columna (ajustar según el diseño)
        hAlign="LEFT",
    )

    # --- Estilos de la tabla
    header_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),       # alinear todo arriba
            ("ALIGN", (0, 0), (0, 0), "LEFT"),         # columna izquierda alineada izq.
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),        # columna derecha alineada der.
            # Bordes guías (útil en pruebas, puedes quitarlos luego)
            # ("BOX", (0,0), (-1,-1), 0.25, colors.grey),
            # ("INNERGRID", (0,0), (-1,-1), 0.25, colors.grey),
        ])
    )

    # --- Flujo de contenido
    flow = [img,Spacer(1,15),header_table, Spacer(1, 20)]

    style_right = ParagraphStyle(name="right", alignment=TA_RIGHT)
    #style_bold_right = ParagraphStyle(name="bold_right", alignment=TA_RIGHT, fontName="Helvetica-Bold")
    # Tabla de conceptos
    table_data = [["Concepto", "Cantidad", "Precio unitario", "Subtotal"]]
    for it in items:
        table_data.append([
            it.concept.name,
            str(it.quantity),
            money(it.unit_price),
            money(it.subtotal)
        ])

    #table_data.append([Paragraph("Subtotal:", style_right), "", "", receipt.subtotal])
    #table_data.append([Paragraph("IVA 16%:", style_right), "", "", "10"])
    table_data.append([Paragraph("<b>Total:</b>", style_right), "", "", receipt.total_amount])

    tbl = Table(table_data, colWidths=[90*mm, 25*mm, 35*mm, 35*mm], hAlign="LEFT")

    tbl.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.25, colors.gray),             # bordes
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#861F3C')),  # fondo encabezado
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),                      # todo a la derecha
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        
        # Filas de totales: que el texto abarque las 3 primeras columnas
        #('SPAN', (0, len(table_data)-3), (2, len(table_data)-3)),  # Subtotal
        #('SPAN', (0, len(table_data)-2), (2, len(table_data)-2)),  # IVA
        ('SPAN', (0, len(table_data)-1), (2, len(table_data)-1)),  # Total
        
        # Fondo gris para la fila del Total
        ('BACKGROUND', (0, len(table_data)-1), (-1, len(table_data)-1), colors.HexColor('#EFEFEF')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),  # encabezado en negrita
    ]))
    flow.append(tbl)

    #doc.build(flow)
    # Añadir pie en todas las páginas
    doc.build(flow, onFirstPage=draw_footer, onLaterPages=draw_footer)    

    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')

    filename = f"factura_{factura['folio']}.pdf"
    response['Content-Disposition'] = ('attachment' if download else 'inline') + f'; filename="{filename}"'
    return response    
