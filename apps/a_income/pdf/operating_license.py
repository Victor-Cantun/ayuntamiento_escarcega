import io
from reportlab.platypus import Table, TableStyle, Paragraph,SimpleDocTemplate, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import qrcode
from reportlab.lib.units import mm
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.graphics.barcode import createBarcodeDrawing
from django.http import HttpResponse
from reportlab.lib.units import cm
from django.contrib.staticfiles import finders
#from reportlab.platypus import SimpleDocTemplate, Spacer
#from reportlab.graphics.shapes import Drawing
#from reportlab.lib.styles import getSampleStyleSheet
#from reportlab.platypus import ()
#from reportlab.platypus import Image
#from reportlab.graphics.barcode import code128
#from reportlab.lib import colors
#from reportlab.pdfgen import canvas
#from reportlab.lib.utils import ImageReader
#import io
#from reportlab.lib.pagesizes import A4
#from reportlab.lib.units import mm
#from decimal import ROUND_HALF_UP
#from reportlab.lib.enums import TA_RIGHT
#from decimal import Decimal
#from reportlab.platypus import Image
#from reportlab.lib.units import inch
#from reportlab.lib.pagesizes import letter
#from reportlab.lib.units import mm
#from reportlab.graphics.barcode import code128
#from datetime import datetime, time
#from reportlab.lib.pagesizes import A4
#from reportlab.lib.units import mm

#from reportlab.lib import colors
PAGE_WIDTH, PAGE_HEIGHT = A4


def draw_watermark(canvas, doc, image_path):
    width, height = A4
    # 70% del ancho y alto de la hoja
    target_width = width * 0.70
    target_height = height * 0.70
    # Guardar estado del lienzo
    canvas.saveState()
    # Transparencia del watermark (1.0 = opaco, 0.0 = invisible)
    canvas.setFillAlpha(0.15)
    # Calcular posición centrada
    x = (width - target_width) / 2
    y = (height - target_height) / 2
    # Dibujar imagen como watermark
    canvas.drawImage(
        image_path,
        x,
        y,
        width=target_width,
        height=target_height,
        preserveAspectRatio=True,
        mask='auto'
    )
    canvas.restoreState()


def generar_qr(data):
    qr = qrcode.QRCode(box_size=3, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img_qr = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img_qr.save(buffer, format="PNG")
    buffer.seek(0)

    return Image(buffer, width=35*mm, height=35*mm)  # Tamaño del QR

def draw_footer(c, doc, folio, uuid):
    width, height = doc.pagesize
    styles = getSampleStyleSheet()

    # --------- Estilos -----
    style_gray = styles["Normal"]
    style_gray.alignment = 1
    style_gray.fontName = "Helvetica-Bold"
    style_gray.textColor = colors.whitesmoke

    style_red = styles["Normal"]
    style_red.alignment = 1
    style_red.fontName = "Helvetica-Bold"
    style_red.textColor = colors.red

    style_center = styles["Normal"]
    style_center.alignment = 1
    style_center.fontName = "Helvetica-Bold"
    style_center.textColor = colors.black

    # --------- QR + URL -----
    qr_img = generar_qr(folio)
    url = Paragraph("www.tramites.escarcega.gob.mx", styles["Normal"])

    qr_table = Table([[qr_img]], colWidths=[45*mm])

    qr_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ]))

    # --------- Columna folio/uuid -----
    #folio_label = Paragraph("Folio Pago", style_gray)
    #folio_label = Paragraph("Folio Pago")
    #folio_value = Paragraph(folio, style_red)

    #uuid_label = Paragraph("UUID", style_gray)
    #uuid_label = Paragraph("UUID")
    #uuid_value = Paragraph(uuid, style_red)

    second_col = Table([
        ["FOLIO PAGO"],
        [folio],
        ["UUID"],
        [uuid],[url]
    ], colWidths=[80*mm])

    second_col.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BACKGROUND", (0,0), (0,0), colors.HexColor("#818080")),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ("BACKGROUND", (0,2), (0,2), colors.HexColor("#818080")),
        ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
        ("TEXTCOLOR", (0,0), (0,0), colors.whitesmoke),
        ("TEXTCOLOR", (0,2), (0,2), colors.whitesmoke),
        ("TEXTCOLOR", (0,1), (0,1), colors.red),
        ("TEXTCOLOR", (0,3), (0,3), colors.red),
        ("ALIGN", (0,0), (0,0), "CENTER"),
        ("ALIGN", (0,2), (0,2), "CENTER"),
    ]))

    # --------- Columna Firma -----
    firma_label = Paragraph("TESORERO MUNICIPAL", style_center)
    firma_nombre = Paragraph("LIC. EDMUNDO PÉREZ GUTIÉRREZ", style_center)

    firma_space = Spacer(1, 5*mm)  # Espacio entre etiqueta y línea
    #bottom_space = Spacer(1, 12*mm)  # Espacio antes del nombre

    firma_table = Table([
        [firma_label],
        [firma_space],
        [firma_nombre]
    ], colWidths=[60*mm])

    firma_table.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        # ✅ Línea de firma colocada JUSTO antes del nombre
        ("LINEABOVE", (0,2), (0,2), 1.5, colors.black),
    ]))

    # -------- Footer Table -------
    footer_table = Table([
        [qr_table, second_col, firma_table]
    ], colWidths=[48*mm, 82*mm, 68*mm])

    footer_table.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ]))

    # Centrado sin salirse del A4
    total_width = sum([48*mm, 82*mm, 68*mm])
    x = (width - total_width) / 2
    y = 20 * mm

    footer_table.wrapOn(c, width, height)
    footer_table.drawOn(c, x, y)

    c.setTitle("Licencia de Funcionamiento")



def generate_license_receipt(request,license,download=False):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Licencia de fuuncionamiento.pdf"'    
    buffer = io.BytesIO()
    # Crear el documento en A4 o letter
    doc = SimpleDocTemplate(buffer, pagesize=A4,leftMargin=1*cm,
        rightMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,)  # puedes cambiar A4 -> letter
    
    elements = []
    styles = getSampleStyleSheet()
    #LOGO de administración
    logo_izq_path=finders.find('images/logo-2.png')
    logo_izq = Image(logo_izq_path, width=2*cm, height=2*cm)
    logo_izq.hAlign = 'LEFT'
    # --- Datos de ejemplo (normalmente vienen de tus modelos)
    empresa = {
        "nombre": "HONORABLE AYUNTAMIENTO DE ESCÁRCEGA",
        "rfc": "MEC910101JL4",
        "direccion": "Calle 29 s/n entree 28 y 31 frente al parque principal, Col. Centro Escárcega, Campeche, C.P. 24350",
        "telefono": "982 82 4 06 59",
        #"email": "tesoreria@escarcega.com",
    }
    # --- Bloque Derecho: datos de empresa + factura
    data_emisor = [
        [Paragraph(f"<b>{empresa['nombre']}</b>", styles["Normal"])],
        [Paragraph(f"RFC: {empresa['rfc']}", styles["Normal"])],
        [Paragraph(empresa["direccion"], styles["Normal"])],
        [Paragraph(f"Tel: {empresa['telefono']}", styles["Normal"])],
        #[Paragraph(f"Email: {empresa['email']}", styles["Normal"])],
        [Spacer(1, 5)],
    ]    

    header_table = Table(
        [
            [logo_izq, data_emisor]  # una fila con dos columnas
        ],
        colWidths=[250, 250],  # ancho de cada columna (ajustar según el diseño)
        hAlign="CENTER",
    )

    header_table.setStyle(
        TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),       # alinear todo arriba
            ("ALIGN", (0, 0), (0, 0), "CENTER"),         # columna izquierda alineada izq.
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),        # columna derecha alineada der.
        ])
    )

    folio_value = f"PL-{license.folio}"  # Ejemplo, cámbialo por tu valor real

    # ✅ Generar código de barras correctamente
    barcode_drawing = createBarcodeDrawing(
        "Code128",
        value=folio_value,
        barHeight=15*mm,
        barWidth=1,
    )

    date = license.issue_date.date().strftime("%d/%m/%Y")
    #new_date = datetime.strptime(date, "%Y-%m-%d").date()
    razon_social = license.customer.get_full_name()
    nombre_comercial = license.trade_name
    rfc= license.customer.rfc
    ramo = license.bouquet
    telefono = license.customer.cellphone
    giro = license.turn
    domicilio = license.customer.get_direction()
    concepto = license.concept

    data = [["","Folio: PL-2025139"],] #Fila 0
    data.append(["LICENCIA DE FUNCIONAMIENTO",barcode_drawing]) # Fila 1
    data.append(["FECHA",""]) #FILA 2
    data.append([date,""]) #FILA 3
    data.append(["NOMBRE O RAZON SOCIAL",""]) #FILA 4
    data.append([razon_social,""]) #FILA 5
    data.append(["NOMBRE COMERCIAL DEL ESTABLECIMIENTO",""]) #FILA 6
    data.append([nombre_comercial,""]) #FILA 7
    data.append(["RFC","RAMO"]) #FILA 8
    data.append([rfc,ramo]) #FILA 9
    data.append(["TELEFONO","GIRO"]) #FILA 10
    data.append([telefono,giro]) #FIILA 11
    data.append(["DOMICILIO",""]) #FILA 12
    data.append([domicilio,""]) #FILA 13
    data.append(["CONCEPTO",""]) #FILA 14
    data.append([concepto,""]) #FILA 15

    table = Table(data, colWidths=[250,250])
    # Estilo de la tabla
    table.setStyle(TableStyle([
        # ✅ Unir filas 0 a 3 de la columna 1
        ('TEXTCOLOR', (0, 0), (1, 0), colors.red),
        ('SPAN', (1, 1), (1, 3)),
        ('ALIGN', (0, 0), (-1, 3), 'CENTER'),
        #('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('BACKGROUND', (0,2), (0,2), colors.HexColor("#818080")),  # encabezado fila 2
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        #('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0,4), (0,4), colors.HexColor("#818080")),  # encabezado fila 4
        ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 4), (1, 4), colors.whitesmoke),
        ('ALIGN', (0, 4), (-1, 7), 'CENTER'),
        #('GRID', (0, 4), (-1,4), 1, colors.white),
        ("SPAN", (0,4), (1,4)), # Une las columnas de razon social fila 4
        ("SPAN", (0,5), (1,5)), # Une las columnas de razon social fila 5
        #("ALIGN", (0,3), (-1,-1), "CENTER"),
        ('BACKGROUND', (0,6), (0,6), colors.HexColor("#818080")),  # encabezado fila 6
        ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 6), (1, 6), colors.whitesmoke),
        ("SPAN", (0,6), (1,6)), # Une las columnas de nombre comercial FILA 6
        ("SPAN", (0,7), (1,7)), # Une las columnas de nombre comercial FILA 7
        #("ALIGN", (0,5), (-1,-1), "CENTER"),
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor("#818080")),  # encabezado fila 8 RAMO Y RFC
        ('FONTNAME', (0, 8), (-1, 8), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 8), (-1, 8), colors.whitesmoke),  
        ("ALIGN", (0,8), (-1,-1), "CENTER"),   

        ('BACKGROUND', (0,10), (-1,10), colors.HexColor("#818080")),  # encabezado fila teleefono y giro 10
        ('FONTNAME', (0, 10), (-1, 10), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 10), (-1, 10), colors.whitesmoke),  
        ("ALIGN", (0,10), (-1,-1), "CENTER"),   
        ('BACKGROUND', (0,12), (0,12), colors.HexColor("#818080")),  # encabezado fila 12 domicilio
        ('FONTNAME', (0, 12), (-1, 12), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 12), (-1, 12), colors.whitesmoke),
        ("SPAN", (0,12), (1,12)), # Une las columnas de la fila 12 DOMICILIO 
        ("SPAN", (0,13), (1,13)), # Une las columnas de la fila 13 domicilio     
        ('BACKGROUND', (0,14), (0,14), colors.HexColor("#818080")),  # encabezado fila 14 CONCEPTO 14
        ('FONTNAME', (0, 14), (-1, 14), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 14), (-1, 14), colors.whitesmoke),
        ("SPAN", (0,14), (1,14)), # Une las columnas de la fila CONCEPTO 14
        ("SPAN", (0,15), (1,15)), # Une las columnas de la fila concepto
        ("ALIGN", (0,15), (-1,-1), "CENTER"),                        
    ]))

    elements.append(header_table)
    elements.append(Spacer(1, 10))  # Espacio antes de las firmas
    elements.append(table)

    def on_page(canvas,doc):
        draw_watermark(canvas, doc, "static/images/escarcega.png")  # tu ruta a imagen
        folio_pago = f"C8P-{license.invoice.id}"
        license_uuid = license.uuid
        draw_footer(canvas, doc, folio=folio_pago, uuid=license_uuid)
    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    return response    

