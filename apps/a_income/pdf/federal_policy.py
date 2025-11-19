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
#from reportlab.lib.styles import getSampleStyleSheet
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
def footer(canvas, doc, nombre_izq, nombre_der):
    canvas.saveState()
    canvas.setTitle("Poliza Federal")
    width, height = A4  # ancho y alto de la hoja
    y = 1.5 * inch  
    # Línea y texto centrados para la firma izquierda
    left_x = width * 0.25  # un cuarto del ancho
    canvas.line(left_x - 1*inch, y, left_x + 1*inch, y)
    canvas.drawCentredString(left_x, y - 12,  nombre_izq)
    # Línea y texto centrados para la firma derecha
    right_x = width * 0.75  # tres cuartos del ancho
    canvas.line(right_x - 1*inch, y, right_x + 1*inch, y)
    canvas.drawCentredString(right_x, y - 12, nombre_der)
    canvas.restoreState()

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

def generate_federal_policy_pdf(request,policy,concepts,items,name_izq,name_der,download=False):    
    # Respuesta HTTP como PDF descarga
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="Poliza-Federal.pdf"'
    #visualiza en el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Poliza Federal.pdf"'    

    # Crear el documento en A4 o letter
    doc = SimpleDocTemplate(response, pagesize=A4,leftMargin=1*cm,
        rightMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,)  # puedes cambiar A4 -> letter
    elements = []

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
    fecha_formateada = policy.date.strftime(formato_largo)
    title_doc = f"Poliza de federal {fecha_formateada}"
    header = encabezado_documento(
        logo_izq_path=finders.find('images/escarcega.png'),
        logo_der_path=finders.find('images/logo-2.png'),
        nombre_empresa='H. Ayuntamiento de Escárcega.',
        nombre_documento=title_doc
    )

    #story = [header, Spacer(1, 12)]
    elements.append(header)
    elements.append(Spacer(1,12))

    # Encabezado
    #elements.append(Paragraph("Poliza Federal", estilo_titulo))
    #elements.append(Spacer(1, 12))
    pesos = '$'
    # Datos de ejemplo para la tabla
    data = [["Cuenta", "Nombre", "Debe", "Haber"],] #Encabezado
    #Cuenta de banco
    for it in items:
        amount = '{0} {1:,.2f}'.format(pesos,it.amount)
        data.append([
            it.bank_account.account,
            it.bank_account.description,
            amount,
            "",
        ])
    #Espacio
    data.append(["","","",""])
    #Conceptos
    for it in concepts:
        amount = '{0} {1:,.2f}'.format(pesos,it['total'])
        data.append([
            it['concept__account_number'],
            it['concept__name'],
            "",
            amount,
        ])
    #Espacio
    data.append(["","","",""])
    amount_bank = '{0} {1:,.2f}'.format(pesos,policy.amount_bank) 
    amount_cash = '{0} {1:,.2f}'.format(pesos,policy.amount_cash)
    banco = f"Importe en Banco: { str(amount_bank) }"
    caja = f"Importe en Caja: { str(amount_cash) }"
    data.append([banco,"",caja,""])       
    # Crear tabla
    table = Table(data, colWidths=[80, 200, 80, 80])

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
        ("ALIGN", (1,1), (1,-2), "LEFT"),
        # 🔹 Fusionar celdas en la última fila
        # Supongamos que la última fila es la número 4 (índice 4)
        ("SPAN", (0,-1), (1,-1)),  # Une columnas 1 y 2
        ("SPAN", (2,-1), (3,-1)),  # Une columnas 3 y 4

        # Alineación de texto en las celdas fusionadas
        ("ALIGN", (0,-1), (1,-1), "LEFT"),
        ("ALIGN", (2,-1), (3,-1), "LEFT"),            
    ]))

    elements.append(table)
    elements.append(Spacer(1, 50))  # Espacio antes de las firmas
    # Crear footer con nombres ya cargados
    footer_func = partial(footer, nombre_izq=name_izq, nombre_der=name_der)
    # Construir PDF
    #doc.build(elements)
    #doc.build(elements, onFirstPage=footer, onLaterPages=footer)
    doc.build(elements, onFirstPage=footer_func, onLaterPages=footer_func)
    return response