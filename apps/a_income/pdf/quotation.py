from django.contrib.staticfiles import finders
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle)
from decimal import ROUND_HALF_UP
from reportlab.lib.units import inch
from functools import partial
from django.http import HttpResponse
from decimal import Decimal
from reportlab.lib.units import cm
import locale
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_RIGHT
#import io
#import qrcode
#from django.core.mail import EmailMessage
#from django.http import FileResponse
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter
#from django.http import Http404
#from reportlab.lib.enums import TA_RIGHT
#from django.utils import timezone
#from reportlab.lib.units import mm
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

def draw_footer(canvas, doc, nombre, cargo):
    canvas.saveState()
    canvas.setTitle("Cotización")
    """
    Dibuja un pie de página con una línea horizontal centrada,
    el nombre y el cargo debajo, alineados al centro.
    """
    width, height = A4  # 595 x 842 puntos

    # Coordenadas base del footer
    y_line = 60     # posición vertical de la línea
    y_nombre = 45   # nombre debajo de la línea
    y_cargo = 30    # cargo debajo del nombre

    # Dibujar línea horizontal centrada
    canvas.setLineWidth(1)
    canvas.line(150, y_line, width - 150, y_line)

    # Configurar fuente
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawCentredString(width / 2, y_nombre, nombre)

    canvas.setFont("Helvetica", 10)
    canvas.drawCentredString(width / 2, y_cargo, cargo)


def encabezado_documento(logo_izq_path, logo_der_path, nombre_empresa, nombre_documento):
    """
    Crea un encabezado con logos y título centrado.
    - logo_izq_path: ruta al logo izquierdo (ej. 'static/img/logo1.png')
    - logo_der_path: ruta al logo derecho (ej. 'static/img/logo2.png')
    - nombre_empresa: texto principal
    - nombre_documento: subtítulo o tipo de documento
    """
    #styles = getSampleStyleSheet()
    # --- Imagen izquierda ---
    logo_izq = Image(logo_izq_path, width=2*cm, height=2*cm)
    logo_izq.hAlign = 'LEFT'    
    # --- Imagen derecha ---
    logo_der = Image(logo_der_path, width=2*cm, height=2*cm)
    logo_der.hAlign = 'RIGHT'   
    # --- Texto central ---
    titulo_style = ParagraphStyle(
        name='TituloCentrado',
        fontSize=14,
        leading=16,
        alignment=1,  # centrado
        spaceAfter=4,
        spaceBefore=4,
        textColor=colors.HexColor("#000000"),
    )    
    subtitulo_style = ParagraphStyle(
        name='SubtituloCentrado',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#333333"),
    )
    titulo = Paragraph(f"<b>{nombre_empresa}</b>", titulo_style)
    subtitulo = Paragraph(f"{nombre_documento}", subtitulo_style)    
    titulo_centrado = [titulo, subtitulo]    
    # --- Tabla del encabezado ---
    data = [[logo_izq, titulo_centrado, logo_der]]
    table = Table(data, colWidths=[4*cm, 10*cm, 4*cm])
    
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('BOX', (0,0), (-1,-1), 0, colors.white),  # Sin bordes
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    
    return table

def generate_quotation_pdf(request,quotation,items,download=False):    
    # Respuesta HTTP como PDF descarga
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="Poliza-Federal.pdf"'
    #visualiza en el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Cotizacion.pdf"'    

    # Crear el documento en A4 o letter
    doc = SimpleDocTemplate(response, pagesize=A4,leftMargin=1*cm,
        rightMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,)  # puedes cambiar A4 -> letter
    elements = []

    
    styles = getSampleStyleSheet()




    # Estilos
    #styles = getSampleStyleSheet()
    #estilo_normal = styles["Normal"]
    #estilo_titulo = styles["Heading2"]

    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') 
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'es_ES')
        except locale.Error:
            # Intenta otra variante si las anteriores fallan (ej. en algunos servidores)
            locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
    # Crear encabezado
    formato_largo = "%d de %B de %Y"
    fecha_formateada = quotation.issue_date.strftime(formato_largo)
    title_doc = "Cotización"
    header = encabezado_documento(
        logo_izq_path=finders.find('images/escarcega.png'),
        logo_der_path=finders.find('images/logo-2.png'),
        nombre_empresa='H. Ayuntamiento de Escárcega.',
        nombre_documento=title_doc
    )

    # 🔹 Crear un nuevo estilo basado en "Normal" pero alineado a la derecha
    estilo_derecha = ParagraphStyle(
        name="Derecha",
        parent=styles["Normal"],
        alignment=TA_RIGHT,  # Alineación a la derecha
    )
    #story = [header, Spacer(1, 12)]
    elements.append(header)
    elements.append(Spacer(1,12))
    dependencia = "MUNICIPIO DE ESCÁRCEGA"
    departamento = "TESORERÍA MUNICIPAL"
    folio = quotation.folio
    asunto = quotation.subject
    fecha = f"Escárcega, Campeche a {fecha_formateada}"

    cliente_nombre = quotation.customer.get_full_name()
    cliente_direccion = quotation.customer.get_direction()
    cliente_rfc= quotation.customer.rfc
    cliente_cp = f"CP {quotation.customer.postal_code}, {quotation.customer.municipality}"
    
    introduccion = quotation.introduction

    elements.append(Paragraph(dependencia,estilo_derecha))
    elements.append(Paragraph(departamento,estilo_derecha))
    elements.append(Paragraph(folio,estilo_derecha))
    elements.append(Paragraph(asunto,estilo_derecha))
    elements.append(Paragraph(fecha,estilo_derecha))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(cliente_nombre, styles["Normal"]))
    elements.append(Paragraph(cliente_direccion, styles["Normal"]))
    elements.append(Paragraph(cliente_rfc, styles["Normal"]))
    elements.append(Paragraph(cliente_cp, styles["Normal"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(introduccion, styles["BodyText"]))
    elements.append(Spacer(1, 20))
    # Encabezado
    #elements.append(Paragraph("Poliza Federal", estilo_titulo))
    #elements.append(Spacer(1, 12))
    pesos = '$'
    # Datos de ejemplo para la tabla
    data = [["IMPUESTOS MUNICIPALES", "AÑO 2025"],] #Encabezado
    #Cuenta de banco
    for it in items:
        amount = '{0} {1:,.2f}'.format(pesos,it.total)
        data.append([
            it.concept.name,
            amount,
        ])     
    # Crear tabla
    table = Table(data, colWidths=[300, 80])

    # Estilo de la tabla
    table.setStyle(TableStyle([
        #('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#861F3C')),  # fondo encabezado
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        # 🔹 Alinear a la izquierda la segunda columna (índice 1)
        # desde la segunda fila (índice 1) hasta la penúltima fila (índice -2)
        ("ALIGN", (0,1), (-1,-1), "LEFT"),
        
    ]))

    elements.append(table)

    conclusion = quotation.conclusion

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(conclusion, styles["BodyText"]))


    elements.append(Spacer(1, 50))  # Espacio antes de las firmas
    def on_page(canvas,doc):
        draw_watermark(canvas, doc, "static/images/logo-2.png")  # tu ruta a imagen
        draw_footer(canvas, doc, nombre="", cargo="TESORERÍA DEL H. AYUNTAMIENTO DE ESCÁRCEGA")
        # Crear footer con nombres ya cargados
        #footer_func = partial(footer, nombre="", cargo="TESORERÍA DEL H. AYUNTAMIENTO DE ESCÁRCEGA")
    # Construir PDF
    #doc.build(elements)
    #doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    doc.build(elements, onFirstPage=on_page, onLaterPages=on_page)
    return response