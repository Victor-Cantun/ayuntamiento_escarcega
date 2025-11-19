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
from reportlab.lib.units import mm
from num2words import num2words

def numero_a_letras(numero: float) -> str:
    """
    Convierte un número a letras en español con formato monetario.
    Ejemplo: 1523.75 -> 'Mil quinientos veintitrés pesos 75/100 M.N.'
    """
    try:
        numero = round(float(numero), 2)
    except (ValueError, TypeError):
        return ""

    # Separar parte entera y decimal
    parte_entera = int(numero)
    parte_decimal = int(round((numero - parte_entera) * 100))

    # Convertir parte entera a palabras
    texto_entero = num2words(parte_entera, lang='es').capitalize()

    # Formatear la parte decimal
    texto_decimal = f"{parte_decimal:02d}/100"

    return f"{texto_entero} pesos {texto_decimal} M.N."


def encabezado_documento(logo_admon_path,empresa):
    # --- Imagen izquierda ---
    logo_admon = Image(logo_admon_path, width=2*cm, height=2*cm)
    logo_admon.hAlign = 'LEFT'    
    #titulo = Paragraph(f"<b>{nombre_empresa}</b>", titulo_style)
    #subtitulo = Paragraph(f"{nombre_documento}", subtitulo_style)    
    #titulo_centrado = [titulo, subtitulo]   
    #emisor = ["H. Ayuntamiento de Escárcega", "MEC9101013JL4", "Régimen fiscal"] 
    #data_emisor = "<br/>".join(emisor)  
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    linea1 = Paragraph(f"<b><font size=8>{empresa['nombre']}</font></b>", style)
    linea2 = Paragraph(f"<b><font size=8>{empresa['rfc']}</font></b>", style)
    linea3 = Paragraph("<font size=8>Régimen fiscal</font>", style)
    linea4 = Paragraph(f"<b><font size=8>{empresa['regimen_fiscal']}</font></b>", style)
    linea5 = Paragraph("<font size=8>Número de certificado</font>", style)
    linea6 = Paragraph("<b><font size=8>000010000005096994626</font></b>", style)

    story = [linea1, Spacer(1, 0.5 * mm), linea2, Spacer(1, 0.5 * mm), linea3, Spacer(1, 0.5 * mm), linea4, Spacer(1, 0.5 * mm), linea5, Spacer(1, 0.5 * mm), linea6]  
    # --- Tabla del encabezado ---
    data = [[story, logo_admon, "CFDI DE INGRESO",""],]
    data.append(["","","Serie","Folio"])
    data.append(["","","PP","202210"])
    data.append(["","","Lugar de emisión","Fecha y Hora de emisión"])
    data.append(["","","24350","2022-04-12"])
    table = Table(data, colWidths=[200,90,110,110])
    
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('BOX', (0,0), (-1,-1), 0, colors.white),  # Sin bordes
        #('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('SPAN',(0,0),(0,4)), #une la fila 0 - 4
        ('SPAN',(1,0),(1,4)), #une la fila 1 -4
        #columna 3 y 4
        ('BACKGROUND', (2,0), (-1,0), colors.HexColor("#818080")),
        ('ALIGN', (2, 0), (-1, 0), 'CENTER'),
        ('SPAN',(2,0),(-1,0)), #une la columna 2-4
        ('TEXTCOLOR', (2, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, 0), 8),   

        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),  #fila 2
        ('FONTSIZE', (0, 1), (-1, 1), 8),  # fila 2
        ('FONTSIZE', (0, 2), (-1, 2), 8), #fila 3
        ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'), #fila 4
        ('FONTSIZE', (0, 3), (-1, 3), 8),   #fila 4
        ('FONTSIZE', (0, 4), (-1, 4), 8), #fila 5

        ('LEADING', (2, 1), (-1, -1), 7),             
    ]))
    
    return table

# Estilo centrado
centered_style = ParagraphStyle(
    name="Centered",
    alignment=1,  # 0=izquierda, 1=centro, 2=derecha
    spaceAfter=4,
)
    # Crear la línea de firma como un párrafo con subrayado
def firma(nombre, puesto):
    linea = Paragraph("______________________________", centered_style)
    nombre_parrafo = Paragraph(f"<b>{nombre}</b>", centered_style)
    puesto_parrafo = Paragraph(puesto, centered_style)
    return [linea, Spacer(1, 6), nombre_parrafo, puesto_parrafo]

def generate_invoice_pdf(request, invoice,customer,items, download=False):
    #visualiza en el navegador
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Factura.pdf"'   
    # Crear el documento en A4 o letter
    doc = SimpleDocTemplate(response, pagesize=A4,
        leftMargin=1*cm,
        rightMargin=1*cm,
        topMargin=1*cm,
        bottomMargin=1*cm,)  # puedes cambiar A4 -> letter
    elements = []
    #styles = getSampleStyleSheet() 
    #Crear encabezado   
    #title_doc = "Cotización"
    header = encabezado_documento(
        logo_admon_path=finders.find('images/logo-2.png'),
        empresa = {
        "nombre": "H. AYUNTAMIENTO DE ESCARCEGA",
        "rfc": "MEC910101JL4",
        "regimen_fiscal":"603.-Personas Morales con Fines no Lucrativos",
        "direccion": "Calle 29 entre 28 y 31 S/N Col. Centro, Escárcega, Campeche, C.P. 24350",
        "telefono": "9828240659",
        "email": "",
        }
        #nombre_empresa='H. Ayuntamiento de Escárcega.',
        #nombre_documento=title_doc
    )
    elements.append(header)

    data = [["Información Cliente",""],] #Fila 0
    data.append([customer.get_full_name(),"Uso CFDI"]) #FILA 1
    data.append([f"RFC: {customer.rfc}","003.- Gastos en General"]) #FILA 2
    table2 = Table(data, colWidths=[250,250])
    table2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#818080")), 
        ("ALIGN", (0,0), (-1,0), "CENTER"), 
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, 0), 8), 
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(table2)
    small_style = ParagraphStyle(
        name='SmallStyle',
        fontName='Helvetica',
        fontSize=8,
        leading=10,             # espacio entre líneas
        wordWrap='CJK',         # 🔹 esto permite el ajuste automático del texto
        )
    
    metodo_pago = invoice.payment_method
    subtotal = invoice.subtotal
    total = invoice.total_amount
    forma_pago = invoice.payment_form.name
    data2 = [["Código","Clave","Descripción","Valor Unitario","Cantidad","Importe","Descuento"],] #Fila 0
    for item in items:
        #descripcion = ("Demas certificados, certificaciones y constancias ...")
        codigo = item.concept.account_number
        clave = "E48"
        descripcion = item.concept.name
        valor_unitario = item.unit_price
        cantidades = item.quantity
        importe = item.total
        data2.append([codigo,clave,Paragraph(descripcion, small_style),valor_unitario,cantidades,importe,""]) #FILA 1
        data2.append(["","","","","","Subtotal:",subtotal])
        data2.append(["","","","","","Total:",total])

    table3 = Table(data2, colWidths=[60,60,150,60,50,60,60])
    table3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#818080")), 
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, 0), 8), 
        ('FONTSIZE', (0, 1), (-1, -1), 8), 
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#818080")), 
    ]))
    elements.append(table3)

    data3 = [["Metodo de pago","Forma de pago","Tipo de Cambio"],]
    data3.append([metodo_pago,forma_pago,""])
    data3.append(["Cantida en Letras","",""])

    cantidad = total
    texto_cantidad = numero_a_letras(cantidad)
    
    data3.append([Paragraph(f"Son: {texto_cantidad}", small_style),"",""])
    table4 = Table(data3, colWidths=[300,100,100])
    table4.setStyle(TableStyle([
        ("ALIGN", (0,0), (-1,-1), "LEFT"),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
        ('FONTSIZE', (0, 0), (-1, 0), 8), 
        ('FONTSIZE', (0, 1), (-1, -1), 8), 
        ('LEADING', (0, 0), (-1, -1), 7),
    ]))
    elements.append(table4)




    # Contenido de la tabla
    data4 = [
        ["", firma(invoice.employee.profile.displayname, invoice.employee.profile.job_title)],
    ]

    # Crear la tabla
    table5 = Table(data4, colWidths=[250, 250])

    # Estilo de la tabla
    table5.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('ALIGN', (1, 0), (1, 0), 'CENTER'),  # Centra el contenido en la celda
    #('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    #('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
    ]))

    elements.append(table5)

    def on_page(canvas,doc):
        canvas.setTitle("Factura")

    doc.build(elements,onFirstPage=on_page, onLaterPages=on_page)
    return response    
