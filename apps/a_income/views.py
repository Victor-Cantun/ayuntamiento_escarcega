from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.a_income.forms import (AccountForm, BankForm, CashPolicyForm, CashRegisterForm, ColonyForm, ConceptForm, CurrencyForm, CustomerForm, FederalPolicyForm, IncomeTypeForm, LicenseForm, PaymentForm_Form, PaymentMethodForm, PaymentStatusForm, PredialForm, InvoiceForm, InvoiceItemForm, QuotationForm, catalogCategoryForm,catalogConceptForm,catalogSubcategoryForm,personMoralForm,personPhysicalForm)
from apps.a_income.models import Bank, BankAccount, Cart, CartItem, CashPolicy, CashRegister, CashierSession, Category, Colony, Concept, ConceptTax, Currency, Customer, FederalPolicy, FederalPolicyItem, IncomeType, OperatingLicense, PaymentForm, PaymentMethod, PaymentStatus, PolicyPredialItem, CashPolicyReceipt, Predial, Invoice, InvoiceItem, Quotation, QuotationItem, Subcategory, Tax
from django.db.models.functions import Concat
from django.db.models import Value, CharField
#datatable
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound, JsonResponse
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.db import IntegrityError
from django.http import HttpResponse
from decimal import Decimal
from django.shortcuts import redirect
from django.db.models import Sum
from django.db.models import Min, Max
from datetime import datetime, time
#from django.http import HttpResponseBadRequest
#pdf y email
from django.core.mail import EmailMessage
#import io
from django.http import Http404
from django.utils import timezone
# Create your views here.
#stripe
import stripe
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.template.loader import render_to_string
from .pdf.utils import generate_pdf_receipt
from .pdf.receipt import generate_payment_receipt_pdf
from .pdf.federal_policy import generate_federal_policy_pdf
from .pdf.cash_policy import generate_cash_policy_pdf
from .pdf.operating_license import generate_license_receipt
from .pdf.quotation import generate_quotation_pdf
from .pdf.invoice import generate_invoice_pdf
#from datetime import datetime, time
#from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
import facturama
from requests.auth import HTTPBasicAuth
import requests
from apps.a_users.models import Profile

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
import pytz
import json
import base64
import os
# utils.py

def facturama_xml(reequest):
    username = "vicodev"
    password = "VicoDev25"
    cfdi_id = "DuDAMmYVnNT7dZa4Pa3ckQ2"  # reemplaza por tu id
    facturama._credentials = (username, password)
    facturama.sandbox = True
    #html_file = facturama.Cfdi.saveAsHtml('7eo51BvzV-E16gBx3nnxfQ2', 'nombreArchivo.html')
    pdf_file = facturama.Cfdi.saveAsPdf(cfdi_id, 'MiFactura.pdf') 

def consultas_facturama(request):
    username = "vicodev"
    password = "VicoDev25"
    #url = "https://apisandbox.facturama.mx/Catalogs/NameIds" #NameIds
    url = "https://apisandbox.facturama.mx/Catalogs/PaymentForms" #Formas de pago

    response = requests.get(url, auth=HTTPBasicAuth(username, password))
    
    if response.status_code == 200:
        data = response.json()
        print("Catálogo de NameIds:", data)
        return render(request,"admin/income/list.html",{"data":data})
    else:
        print("Error:", response.status_code, response.text)

    return HttpResponse("")        

def facturama_customer_new(request,customer):
    facturama._credentials = ('vicodev', 'VicoDev25')
    facturama.sandbox = True
    print("LLEGO A FACTURAMA")

    customer_object = {
        "Id": customer.id,
        "Email": customer.email,
        "Address": {
            "Street": customer.street,
            "ExteriorNumber": customer.no_ext,
            "InteriorNumber": customer.no_int,
            "Neighborhood": customer.colony.name,
            "ZipCode": customer.postal_code,
            "Locality": customer.colony.city,
            "Municipality": customer.municipality,
            "State": customer.state,
            "Country": customer.country,
        },
        "Rfc": customer.rfc,
        "Name": customer.get_full_name(),
        "CfdiUse": customer.cfdi_use.code,
        "TaxZipCode": customer.postal_code,
        "FiscalRegime": customer.fiscal_regimen.code,
    }

    cliente = facturama.Client.create(customer_object)
    print("Cliente creado",cliente)
    return HttpResponse("")

def facturama_concept_new(request,concept):
    facturama._credentials = ('vicodev', 'VicoDev25')
    facturama.sandbox = True
    print("LLEGO A FACTURAMA")
    taxes = concept.taxes.all()

    product_object = {
            "Unit": concept.Unit,
            "UnitCode": concept.UnitCode.clave_sat,
            "IdentificationNumber": concept.account_number,
            "Name": concept.name,
            "Description": concept.description,
            "Price": float(concept.unit_price),
            "CodeProdServ": concept.CodeProdServ,
            "CodeProdServName": concept.CodeProdServName,
            "Taxes": [
            {
                "Name": item.tax.name,
                "Rate": float(item.tax.rate),
                "IsRetention": item.tax.IsRetention,
                "IsFederalTax": item.tax.IsFederalTax,
                "IsQuota":item.tax.IsQuota,
                "Total": float(item.tax.Total)
            }
            for item in taxes
            ]
            
    }
    product = facturama.Product.create(product_object)
    print("Producto creado",product)
    return HttpResponse("")

def facturama_invoice_new(request, invoice):
    facturama._credentials = ('vicodev', 'VicoDev25')
    facturama.sandbox = True
    print("llego a facturama")
    customer = invoice.customer
    items = invoice.items.all()

    # Obtener la zona horaria configurada en Django
    current_tz = timezone.get_current_timezone()
    issue_date_local = invoice.issue_date.astimezone(current_tz)
    
    invoice_object = {
        "Folio": invoice.folio,
        "Date": issue_date_local.strftime("%Y-%m-%dT%H:%M"),  # Formato sin segundos
        "Currency": invoice.currency.clave,
        "ExpeditionPlace": "24350",
        "CfdiType": "I",
        "PaymentForm": invoice.payment_form.clave,
        "PaymentMethod": invoice.payment_method.clave,
        "Receiver": {
            "Rfc": customer.rfc,
            "Name": customer.get_full_name(),
            "CfdiUse": customer.cfdi_use.code,
            "FiscalRegime": customer.fiscal_regimen.code,
            "TaxZipCode": customer.postal_code
        },
        "Items": []
    }
    
    # Construir items según ejemplo de Facturama
    for product in items:
        item = {
            "ProductCode": product.concept.CodeProdServ,
            "IdentificationNumber": product.concept.account_number,
            "Description": product.concept.description,
            "Unit": product.concept.Unit,
            "UnitCode": product.concept.UnitCode.clave_sat,
            "UnitPrice": float(product.unit_price),
            "Quantity": float(product.quantity),
            "Subtotal": float(product.subtotal),
            "Total": float(product.total)
        }
        
        # Verificar si tiene impuestos
        taxes_list = []
        has_taxes = False
        
        for ct in product.concept.taxes.all():
            has_taxes = True
            tax_total = round(float(product.subtotal) * float(ct.tax.rate), 2)
            
            taxes_list.append({
                "Total": tax_total,
                "Name": ct.tax.get_sat_tax_code_display(),  # Debe ser "IVA", "ISR", "IEPS", etc.
                "Base": float(product.subtotal),
                "Rate": float(ct.tax.rate),
                "IsRetention": ct.tax.IsRetention
            })
        
        # Asignar TaxObject según si tiene impuestos o no
        if has_taxes:
            item["TaxObject"] = "02"  # Sí es objeto de impuestos
            item["Taxes"] = taxes_list
        else:
            item["TaxObject"] = "01"  # No es objeto de impuestos
        
        invoice_object["Items"].append(item)
    
    try:
        # Crear el CFDI
        cfdi = facturama.Cfdi.create3(invoice_object)
        print(cfdi)
                # Extraer información del CFDI
        cfdi_id = cfdi.get('Id')
        uuid = cfdi.get('Complement', {}).get('TaxStamp', {}).get('Uuid')
        
        if not uuid:
            raise Exception("No se pudo obtener el UUID del CFDI")
        
        if not cfdi_id:
            raise Exception("No se pudo obtener el ID del CFDI")
        
        print(f"✓ CFDI creado - ID: {cfdi_id}, UUID: {uuid}")
        
        # Guardar UUID y fecha de timbrado
        invoice.cfdi_id = cfdi_id
        invoice.cfdi_uuid = uuid
        invoice.cfdi_date = timezone.now()
        invoice.cfdi_status = 'active'
        
        # Crear directorio temporal si no existe
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_cfdi')
        os.makedirs(temp_dir, exist_ok=True)
        
        # Nombres de archivos temporales
        pdf_filename = f'cfdi_{invoice.folio}_{uuid}.pdf'
        html_filename = f'cfdi_{invoice.folio}_{uuid}.html'
        xml_filename = f'cfdi_{invoice.folio}_{uuid}.xml'
        
        pdf_temp_path = os.path.join(temp_dir, pdf_filename)
        html_temp_path = os.path.join(temp_dir, html_filename)
        xml_temp_path = os.path.join(temp_dir, xml_filename)
        
        # Guardar archivos usando métodos de Facturama
        print("Generando archivos PDF y HTML...")
        facturama.Cfdi.saveAsPdf(cfdi_id, pdf_temp_path)
        facturama.Cfdi.saveAsHtml(cfdi_id, html_temp_path)
        facturama.Cfdi.saveAsXML(cfdi_id, xml_temp_path)
        
        # Leer archivos generados y guardarlos en el modelo
        with open(pdf_temp_path, 'rb') as pdf_file:
            invoice.cfdi_pdf.save(
                pdf_filename,
                ContentFile(pdf_file.read()),
                save=False
            )
        
        with open(xml_temp_path, 'rb') as xml_file:
            invoice.cfdi_xml.save(
                xml_filename,  # Guardamos HTML como XML temporalmente
                ContentFile(xml_file.read()),
                save=False
            )
        
        # Eliminar archivos temporales
        try:
            os.remove(pdf_temp_path)
            os.remove(xml_temp_path)
        except:
            pass
        
        invoice.save()
        
        print(f"✓ Archivos guardados exitosamente")
        print(f"  - PDF: {invoice.cfdi_pdf.name}")
        print(f"  - XML: {invoice.cfdi_xml.name}")
        
        return cfdi
        
    except facturama.MalformedRequestError as e:
        print(f"\n✗ Error al crear CFDI:")
        print(e)
        raise
    except Exception as e:
        print(f"\n✗ Error inesperado:")
        print(e)
        raise

def download_cfdi_files(cfdi_id):
    """Descarga el XML y PDF de un CFDI desde Facturama usando requests"""
    
    # Credenciales de Facturama
    username = 'vicodev'
    password = 'VicoDev25'
    
    # URLs de la API
    if facturama.sandbox:
        base_url = 'https://apisandbox.facturama.mx'
    else:
        base_url = 'https://api.facturama.mx'
    
    # Autenticación básica
    auth = (username, password)
    
    try:
        # Descargar XML
        xml_url = f'{base_url}/cfdis/xml/issued/{cfdi_id}'
        xml_response = requests.get(xml_url, auth=auth)
        xml_response.raise_for_status()
        xml_content = xml_response.content
        
        # Descargar PDF
        pdf_url = f'{base_url}/cfdis/pdf/issued/{cfdi_id}'
        pdf_response = requests.get(pdf_url, auth=auth)
        pdf_response.raise_for_status()
        pdf_content = pdf_response.content
        
        return xml_content, pdf_content
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error al descargar archivos: {e}")
        raise


@login_required
def invoice_list(request):
    """Lista todas las facturas"""
    invoices = Invoice.objects.all().order_by('-issue_date')
    
    context = {
        'invoices': invoices,
    }
    
    return render(request, 'admin/income/invoices/invoice_list.html', context)

@login_required
def invoice_detail(request, invoice_id):
    """Muestra el detalle de una factura"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    context = {
        'invoice': invoice,
        'items': invoice.items.all(),
        'customer': invoice.customer,
    }
    
    return render(request, 'admin/income/invoices/detail.html', context)

@login_required
def invoice_edit(request, invoice_id):
    """Edita una factura existente"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Verificar que no esté timbrada
    if invoice.cfdi_uuid:
        messages.error(request, 'No se puede editar una factura timbrada')
        return redirect('invoice_detail', invoice_id=invoice.id)
    
    if request.method == 'POST':
        # Tu lógica para editar factura
        # ...
        messages.success(request, 'Factura actualizada exitosamente')
        return redirect('invoice_detail', invoice_id=invoice.id)
    
    context = {
        'invoice': invoice,
    }
    
    return render(request, 'admin/income/invoices/invoice_form.html', context)



@login_required
def invoice_create_cfdi(request, invoice_id):
    print("llego a invoice create")
    """Genera el CFDI y lo envía por correo"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    # Verificar que la factura no esté ya timbrada
    if invoice.cfdi_uuid:
        messages.warning(request, f'Esta factura ya tiene un CFDI timbrado: {invoice.cfdi_uuid}')
        return redirect('income:invoice_detail', invoice_id=invoice.id)
    
    try:
        # Crear el CFDI
        cfdi = facturama_invoice_new(request, invoice)
        
        messages.success(request, f'CFDI creado exitosamente. UUID: {invoice.cfdi_uuid}')
        
        # Enviar por correo si el cliente tiene email
        if invoice.customer.email:
            try:
                #send_cfdi_email(invoice)
                cfdi_id = invoice.cfdi_id
                customer_email = invoice.customer.email
                facturama.Cfdi.send_by_email('issued',cfdi_id,customer_email)
                messages.success(request, f'CFDI enviado al correo: {invoice.customer.email}')
            except Exception as e:
                messages.warning(request, f'CFDI creado pero no se pudo enviar el correo: {str(e)}')
        else:
            messages.info(request, 'El cliente no tiene correo electrónico registrado')
        
        return redirect('income:invoice_detail', invoice_id=invoice.id)
        
    except Exception as e:
        messages.error(request, f'Error al crear el CFDI: {str(e)}')
        return redirect('income:invoice_detail', invoice_id=invoice.id)

def send_cfdi_email(invoice):
    """Envía el CFDI por correo electrónico al cliente"""
    
    if not invoice.cfdi_uuid:
        raise Exception("La factura no tiene un CFDI timbrado")
    
    customer = invoice.customer
    
    # Verificar que el cliente tenga email
    if not customer.email:
        raise Exception("El cliente no tiene un correo electrónico registrado")
    
    # Crear el asunto del correo
    subject = f'Factura Electrónica {invoice.folio} - {invoice.cfdi_uuid}'
    
    # Crear el cuerpo del correo (puedes usar un template HTML)
    message = f"""
    Estimado/a {customer.get_full_name()},
    
    Adjunto encontrará su Factura Electrónica (CFDI 4.0):
    
    Folio: {invoice.folio}
    UUID: {invoice.cfdi_uuid}
    Fecha de emisión: {invoice.issue_date.strftime('%d/%m/%Y %H:%M')}
    Total: ${invoice.total} {invoice.currency.clave}
    
    Los archivos adjuntos son:
    - XML: Archivo oficial del CFDI
    - PDF: Representación impresa de la factura
    
    Gracias por su preferencia.
    
    Saludos cordiales,
    {settings.COMPANY_NAME if hasattr(settings, 'COMPANY_NAME') else 'Tu Empresa'}
    """
    
    # Crear el email
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
    )
    
    # Adjuntar XML
    if invoice.cfdi_xml:
        email.attach_file(invoice.cfdi_xml.path)
    
    # Adjuntar PDF
    if invoice.cfdi_pdf:
        email.attach_file(invoice.cfdi_pdf.path)
    
    # Enviar el correo
    try:
        email.send(fail_silently=False)
        print(f"✓ Correo enviado exitosamente a {customer.email}")
        return True
    except Exception as e:
        print(f"✗ Error al enviar correo: {e}")
        raise

# Versión alternativa con template HTML
def send_cfdi_email_html(invoice):
    """Envía el CFDI por correo con template HTML"""
    
    if not invoice.cfdi_uuid:
        raise Exception("La factura no tiene un CFDI timbrado")
    
    customer = invoice.customer
    
    if not customer.email:
        raise Exception("El cliente no tiene un correo electrónico registrado")
    
    subject = f'Factura Electrónica {invoice.folio}'
    
    # Renderizar template HTML
    html_content = render_to_string('emails/cfdi_email.html', {
        'invoice': invoice,
        'customer': customer,
    })
    
    email = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[customer.email],
    )
    email.content_subtype = 'html'  # Importante para HTML
    
    # Adjuntar archivos
    if invoice.cfdi_xml:
        email.attach_file(invoice.cfdi_xml.path)
    
    if invoice.cfdi_pdf:
        email.attach_file(invoice.cfdi_pdf.path)
    
    try:
        email.send(fail_silently=False)
        print(f"✓ Correo enviado exitosamente a {customer.email}")
        return True
    except Exception as e:
        print(f"✗ Error al enviar correo: {e}")
        raise

@login_required
def invoice_download_xml(request, invoice_id):
    """Descarga el XML del CFDI"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if not invoice.cfdi_xml:
        messages.error(request, 'Esta factura no tiene XML disponible')
        return redirect('income:invoice_detail', invoice_id=invoice.id)
    
    return FileResponse(
        invoice.cfdi_xml.open('rb'),
        as_attachment=True,
        filename=f'cfdi_{invoice.folio}_{invoice.cfdi_uuid}.xml'
    )

@login_required
def invoice_download_pdf(request, invoice_id):
    """Descarga el PDF del CFDI"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if not invoice.cfdi_pdf:
        messages.error(request, 'Esta factura no tiene PDF disponible')
        return redirect('income:invoice_detail', invoice_id=invoice.id)
    
    return FileResponse(
        invoice.cfdi_pdf.open('rb'),
        as_attachment=True,
        filename=f'cfdi_{invoice.folio}_{invoice.cfdi_uuid}.pdf'
    )

@login_required
def invoice_resend_email(request, invoice_id):
    """Reenvía el CFDI por correo electrónico"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if not invoice.cfdi_uuid:
        messages.error(request, 'Esta factura no tiene un CFDI timbrado')
        return redirect('income:invoice_detail', invoice_id=invoice.id)
    
    try:
        send_cfdi_email(invoice)
        messages.success(request, f'CFDI reenviado exitosamente a: {invoice.customer.email}')
    except Exception as e:
        messages.error(request, f'Error al enviar el correo: {str(e)}')
    
    return redirect('income:invoice_detail', invoice_id=invoice.id)

@login_required
def invoice_cancel_cfdi(request, invoice_id):
    """Cancela un CFDI"""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    
    if request.method == 'POST':
        cancellation_reason = request.POST.get('reason', '02')
        
        try:
            cancel_cfdi(invoice, cancellation_reason)
            messages.success(request, f'CFDI cancelado exitosamente. UUID: {invoice.cfdi_uuid}')
        except Exception as e:
            messages.error(request, f'Error al cancelar el CFDI: {str(e)}')
        
        return redirect('income:invoice_detail', invoice_id=invoice.id)
    
    # Renderizar formulario de confirmación
    return render(request, 'admin/income/invoices/cancel_cfdi.html', {'invoice': invoice})    

def cancel_cfdi(invoice, cancellation_reason='02'):
    """
    Cancela un CFDI en Facturama
    
    Motivos de cancelación:
    01 - Comprobante emitido con errores con relación
    02 - Comprobante emitido con errores sin relación
    03 - No se llevó a cabo la operación
    04 - Operación nominativa relacionada en la factura global
    """
    
    if not invoice.cfdi_uuid:
        raise Exception("La factura no tiene un CFDI timbrado")
    
    if invoice.cfdi_status == 'cancelled':
        raise Exception("El CFDI ya está cancelado")
    
    facturama._credentials = ('vicodev', 'VicoDev25')
    facturama.sandbox = True
    
    try:
        # Cancelar en Facturama
        cancellation_data = {
            "motive": cancellation_reason,
            "uuidReplacement": None  # Si hay factura de reemplazo, poner UUID aquí
        }
        
        response = facturama.Cfdi.cancel(invoice.cfdi_uuid, cancellation_data)
        
        # Actualizar el estado en la base de datos
        invoice.cfdi_status = 'cancelled'
        invoice.cfdi_cancellation_date = timezone.now()
        invoice.save()
        
        print(f"✓ CFDI cancelado exitosamente - UUID: {invoice.cfdi_uuid}")
        
        return response
        
    except Exception as e:
        print(f"✗ Error al cancelar CFDI: {e}")
        raise

def check_cancellation_status(invoice):
    """Verifica el estado de cancelación de un CFDI"""
    
    if not invoice.cfdi_uuid:
        raise Exception("La factura no tiene un CFDI timbrado")
    
    facturama._credentials = ('vicodev', 'VicoDev25')
    facturama.sandbox = True
    
    try:
        # Consultar estado en el SAT
        status = facturama.Cfdi.cancellationStatus(invoice.cfdi_uuid)
        
        return status
        
    except Exception as e:
        print(f"✗ Error al consultar estado: {e}")
        raise

@login_required
def income_view(request):
    #Obtener sesion
    caja_id = request.session.get('caja_id')
    caja_nombre = request.session.get('caja_nombre')
    caja_status = request.session.get('caja_status')

    if caja_id and caja_status == 'active':
        print("caja activa",caja_nombre)
        #return HttpResponse(f"💰 Caja activa: {caja_nombre}")
        context ={"caja_activa":caja_nombre}
    else:
        print("No hay caja activa")
        #return HttpResponse("⚠️ No hay caja activa actualmente.")
    #except CashRegister.DoesNotExist:
        print("No ha iniciado caja")
        cajas_disponibles = CashRegister.objects.filter(status = 'deactivate')
        if cajas_disponibles.exists():
            context = {"cajas_disponibles":cajas_disponibles}
        else :
            context = {"cajas_disponibles":""}
    

    return render(request, "admin/income/payment/index.html",context)

@login_required
def cash_register_start(request):
    cash_register_id = request.POST.get("cash_register")
    if not cash_register_id:
        message = "Selecciona una caja"
        context = {
            'message':message
        }
        return render(request, "admin/income/cash_registers/error.html",context)        
    else:
        try:
            caja = CashRegister.objects.get(id=cash_register_id, status="deactivate")
            print("Actualizo el estatus de la caja a activo e inicio sesión")
            caja.status = "active"
            caja.employee_id = request.user.id
            caja.save()
            sesion_start = CashierSession.objects.create(cash_register_id = caja.id, employee_id = request.user.id)
            sesion_start.save()
            message = "Inicio de Caja exitoso, ya puedes cobrar"
            # Guarda la sesión
            request.session['caja_id'] = caja.id
            #request.session['caja_key'] = caja.key
            request.session['caja_nombre'] = caja.name
            request.session['caja_status'] = 'active'

            context = {
                'message':message
            }
            response = render(request, "admin/income/cash_registers/success.html",context)
            #response["HX-Trigger"] = "ReloadPage"
            return response 
            #return redirect('income:start')

        except CashRegister.DoesNotExist:
            print("La caja ya está activa, no puede iniciar sesión")    
            message = "La caja ya esta activa, selecciona otra caja para poder cobrar"
            context = {
                'message':message
            }
            return render(request, "admin/income/cash_registers/error.html",context)        


    #si caja_seleccionada esta desactivada
    #guarda el inicio de sesion y cambia el estatus de la caja
    #cierra el model o redirige al cobro

@login_required
def closing_reigster(request):
    caja_id = request.session.get('caja_id')

    if caja_id:
        try:
            caja = CashRegister.objects.get(id=caja_id)
            caja.status = 'deactivate'
            caja.employee = None
            caja.save()
        except CashRegister.DoesNotExist:
            pass

        # Elimina la sesión
        request.session.pop('caja_id', None)
        request.session.pop('caja_nombre', None)
        request.session.pop('caja_status', None)
        return redirect('account_logout')
        #return HttpResponse("🔒 Sesión de caja cerrada correctamente.")
    else:
        return HttpResponse("⚠️ No hay sesión de caja activa.")


@login_required
def income_payment_customer_new(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit = False)
            customer.employee_id = request.user.id
            customer.save()
            message = "Registro realizado correctamente"
            customer = get_object_or_404(Customer, id=customer.id)
            facturama_customer_new(request,customer)
            receipt_form = InvoiceForm(initial = {'customer':customer.id,'pay_form':'cash','payment_method':'PUE','payment_status':'PAGADO'}) 
            context = {
                'message':message,
                'customer':customer,
                'receipt_form':receipt_form
            }
            return render(request, "admin/income/payment/new.html",context)      
        else:
            message = "Existen errores en el formulario"
            context = {
                'message':message,
                'form':form,
            }
            return render(request,"admin/income/payment/customer_new.html",context)
    else:
        form = CustomerForm()
        return render(request, "admin/income/payment/customer_new.html", {"form": form})

@login_required
def income_payment_person_type(request):
    return render(request, "admin/income/customer/customer_type.html")

@login_required
def income_payment_customer_save(request):
    if request.method=="POST":
        person_type = int(request.POST["person_type"])
        #print("tipo de persona:",person_type)
        if person_type == 1:
            #print("tipo de persona fisica:",person_type)
            customer_form = personPhysicalForm(request.POST)
            template = "admin/income/customer/person_physical.html"
        if person_type == 2:
            #print("tipo de persona moral:",person_type)
            customer_form = personMoralForm(request.POST)
            template = "admin/income/customer/person_moral.html"
        if customer_form.is_valid():
            customer = customer_form.save()
            #customer = get_object_or_404(Customer, id=customer.id)
            return redirect("receipt_new",customer_id = customer.id)
        else:
            return render(request,template,{"form":customer_form})
    else:
        return HttpResponse("")        

@login_required
def income_payment_customer_search(request):
    if request.method == "POST":
        name_input = request.POST["name"]
        #print("valor: ",type(name_input))
        if name_input != '':
            customers = Customer.objects.annotate(
                nombre_completo=Concat("name",Value(" "),"paternal_surname",Value(" "),"maternal_surname",output_field=CharField(),)
            ).filter(nombre_completo__icontains=name_input)[:10]
            if customers.exists():
                return render(request, "admin/income/payment/customers_list.html", {"customersList": customers})
            else:
                return render(request, "admin/income/payment/doesnot_exist_customers.html", {"name": name_input})
        else:
            return HttpResponse('')
    else:
        return render(request, "admin/income/payment/customer_search.html")

@login_required
def income_payment_customer_edit(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        #print("llego al post")
        if customer.person_type == 1:
            customer_form = personPhysicalForm(request.POST, instance=customer)
            template = "admin/income/payment/edit_person_physical.html"
        if customer.person_type == 2:
            customer_form = personMoralForm(request.POST, instance=customer)
            template = "admin/income/payment/edit_person_moral.html"
        if customer_form.is_valid():
            #print("es valido")
            customer = customer_form.save(commit=False)
            customer.employee_id = request.user.id
            customer.save()
            message = "Registro actualizado correctamente"
            context = {
                'message':message,
                'customer':customer
            }
            response = render(request, "admin/income/payment/customer_detail.html", context)
            #response["HX-Trigger"] = "UpdateCustomer"
            return response            
        else:
            #print("no es valido")
            return render(request,template,{"form":customer_form, "model": customer})      
    else:
        if customer.person_type == 1:
            form = personPhysicalForm(instance=customer)
            template = "admin/income/payment/edit_person_physical.html"
        if customer.person_type == 2:
            form = personMoralForm(instance=customer)
            template = "admin/income/payment/edit_person_moral.html"
    return render(request,template,{"form": form, "model": customer})   

@login_required
def income_payment_customer_detail(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request,"admin/income/payment/customer_detail.html",{"customer": customer})  

@login_required
def income_payment_receipt_new(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    #user = request.user.id
    #new_customer = request.user.customer
    #print("cliente:",new_customer.id)
    receipt_form = InvoiceForm(initial = {'customer':customer.id,'pay_form':'cash','payment_method':'PUE','payment_status':'pagado'}) 
    context = {
        'customer':customer,
        'receipt_form':receipt_form
    }
    return render(request, "admin/income/payment/new.html",context)

@login_required
def income_payment_concept_search(request):
    #q = request.GET.get("q", "")
    #conceptos = Concept.objects.filter(name__icontains=q).values("id", "name","unit_price")[:10]
    #return JsonResponse(list(conceptos), safe=False)
    q = request.GET.get("q", "")

    conceptos = Concept.objects.filter(name__icontains=q).prefetch_related("taxes")[:10]

    results = []
    for c in conceptos:
        results.append({
            "id": c.id,
            "name": c.name,
            "unit_price": float(c.unit_price),
            "taxes": [
                
                {
                    
                    "id": t.tax.id,
                    "name": t.tax.name,
                    "rate": float(t.tax.rate),
                    "is_retention": t.tax.IsRetention,
                    "is_federal_tax": t.tax.IsFederalTax,
                    "is_quota":t.tax.IsQuota,
                    "sat_tax_code": t.tax.sat_tax_code,
                    "factor_type": t.tax.factor_type,

                } 
                for t in c.taxes.all()
                    
            ]
        })

    return JsonResponse(results, safe=False)    

@login_required
def pay_select_concept(request):
    if request.method == "POST":
        category = request.POST["id_category"]
        print(category)
        #pass
        concepts = Concept.objects.all().filter(category_id = category)
    return render(request, "admin/income/pay/select_concept.html",{"concepts":concepts})

@login_required
def income_payment_receipt_save(request):
    if request.method == "POST":
        # 1. Guardar pago
        invoice = InvoiceForm(request.POST)
        if invoice.is_valid():
            invoice = invoice.save(commit=False)
            invoice.employee_id = request.user.id
            invoice.cash_register_id = request.session.get('caja_id')
            invoice.cfdi_status = 'draft'
            invoice.save()
            # 2. Obtener listas de IDs de conceptos y precios
            concepto_ids = request.POST.getlist("concepto_id[]")
            cantidades = request.POST.getlist("cantidad[]")
            precios = request.POST.getlist("precio[]")
            descuentos = request.POST.getlist("descuento[]")
            impuestos = request.POST.getlist("impuesto[]")
            subtotales = request.POST.getlist("subtotal[]")
            totales = request.POST.getlist("total[]")
            #subtotales = request.POST.getlist("subtotal[]")
            # 3. Recorrer y crear los items
            for c_id, quantity,unit_price, descuento, impuesto, subtotal, total in zip(concepto_ids,cantidades, precios, descuentos, impuestos, subtotales,totales):
                if c_id:  # solo si el concepto tiene un id válido
                    InvoiceItem.objects.create(
                        invoice_id=invoice.id,
                        concept_id=c_id,   
                        quantity = float(quantity),
                        unit_price=float(unit_price) or 0,
                        discount_amount = float(descuento) or 0,
                        tax_amount = float(impuesto) or 0,
                        subtotal = float(subtotal),
                        total = float(total)
                        #subtotal = float(subtotal)
                    )
            # 4. Redirigir a un detalle de factura o a una lista
            context = {'receipt_id':invoice.id}
            print("pago guardado")
            #facturama_invoice_new(request,invoice)
            return redirect('income:invoice_create_cfdi', invoice_id=invoice.id)
            #return render(request,"admin/income/payment/payment_success.html",context)
        else:
            #Obtener el cliente en caso de que el pago no sea valido, volver a intentar
            customer_id = request.POST["customer"]
            customer = get_object_or_404(Customer, pk=customer_id)
            context = {
                'customer':customer,
                "receipt_form":invoice
            }
            return render(request, "admin/income/payment/new.html",context)

@login_required
def income_payment_receipt_detail(request,pk):
    PaymentReceipt = get_object_or_404(Invoice, pk=pk)
    ReceiptItems = PaymentReceipt.items.all()
    print(ReceiptItems)
    return render(request,"admin/income/payment/receipt_detail.html",{"receipt":PaymentReceipt,"items":ReceiptItems})

@login_required
def income_payment_receipt_pdf(request, receipt_id, download=False):
    try:
        receipt = get_object_or_404(Invoice, pk=receipt_id)
        customer = receipt.customer
        items = receipt.items.all()
        print("items:",items)
        return generate_payment_receipt_pdf(request, receipt,customer,items, download=False)
    except Invoice.DoesNotExist:
        raise Http404("Factura no encontrada")

@login_required
def income_payment_invoice_pdf(request, invoice_id, download=False):
    try:
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        customer = invoice.customer #Obtengo datos del cliente
        items = invoice.items.all() #Obtengo los items de la factura
        return generate_invoice_pdf(request, invoice,customer,items, download=False)
    except Invoice.DoesNotExist:
        raise Http404("Factura no encontrada")    

@login_required
def income_cancel_invoice(request, invoice_id): 
    model = get_object_or_404(Invoice, pk = invoice_id)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/reports/success.html",{"message": message},)
            #response["HX-Trigger"] = "UpdateCategoriesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/reports/error.html",{"message": message},)
        #response["HX-Trigger"] = "UpdateCategoriesList"
        return response    
    return render(request, "admin/income/reports/cancel.html", {"model": model})                  

@login_required
def licenses_view(request):
    return render(request, "admin/income/licenses/index.html")

@login_required
def licenses_customer_search(request):
    if request.method == "POST":
        name_input = request.POST["name"]
        #print("valor: ",type(name_input))
        if name_input != '':
            customers = Customer.objects.annotate(
                nombre_completo=Concat("name",Value(" "),"paternal_surname",Value(" "),"maternal_surname",output_field=CharField(),)
            ).filter(nombre_completo__icontains=name_input)[:10]
            if customers.exists():
                return render(request, "admin/income/licenses/customers_list.html", {"customersList": customers})
            else:
                return render(request, "admin/income/licenses/doesnot_exist_customers.html", {"name": name_input})
        else:
            return HttpResponse('')
    else:
        return render(request, "admin/income/licenses/customer_search.html")
    
@login_required
def license_new(request):
    return render(request, "admin/income/licenses/new.html")

@login_required
def folio_search(request):
    if request.method == "POST":
        folio = request.POST.get('pay_folio')
        try:
            invoice = get_object_or_404(Invoice, pk=folio)
        except Exception as e:
            print("error",e)
            return render(request, "admin/income/licenses/not_found.html")
        
        license_form = LicenseForm(initial={'customer':invoice.customer,'invoice':invoice})
        customer = invoice.customer
        #invoice = invoice
        items = invoice.items.all()
        #print(items)
        context = {
            'form':license_form,
            'customer':customer,
            'invoice':invoice,
            'items':items
        }
        return render(request, "admin/income/licenses/form_license.html",context)

@login_required
def license_save(request):
    if request.method == "POST":
        license = LicenseForm(request.POST)
        if license.is_valid():
            license = license.save(commit=False)
            license.employee_id = request.user.id
            license.save()
            context = {'license_id':license.id}
            return render(request,"admin/income/licenses/license_success.html",context)
        else:
            context = {
                "form":license
            }
            return render(request, "admin/income/licenses/new.html",context)

@login_required
def operating_license_pdf(request,license_id):        
        try:
            license = get_object_or_404(OperatingLicense, pk=license_id)
            #print("licencia",license)
            # usa el dict de ejemplo o tu propio mapeo
            return generate_license_receipt(request,license,download=False)
            #response = HttpResponse(pdf_bytes, content_type='application/pdf')
            #return response            
            ##response['Content-Disposition'] = 'inline; filename="licencia_funcionamiento.pdf"'
        except Exception as e:
            print("error",e)
            return render(request, "admin/income/licenses/not_found.html")

@api_view(["GET"])
@permission_classes([AllowAny])
def validate_license(request,license_uuid):
    try:
        license = get_object_or_404(OperatingLicense, uuid=license_uuid)
        context = {'license_id':license.id}
        return render(request,"admin/income/licenses/license_success.html",context)
    except Exception as e:
        return render(request, "admin/income/licenses/not_found.html")
        
@login_required
def operating_licenses_list(request):
    if request.method == "POST":

        start = request.POST.get("start_date")
        end = request.POST.get("end_date")

        if start and end:

            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            start_date = timezone.make_aware(datetime.combine(start_date, time.min))
            end_date = timezone.make_aware(datetime.combine(end_date, time.max))

            licenses = OperatingLicense.objects.filter(issue_date__range=(start_date, end_date))
            
            context = {'licenses':licenses} 

            return render(request, "admin/income/licenses/list.html", context) 
        else:
            return HttpResponse("")       
    else:
        # Inicio del día (00:00:00)
        inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # Fin del día siguiente (00:00:00)
        fin = inicio + timedelta(days=1)
        # Consulta de todos los registros del día actual
        licenses = OperatingLicense.objects.filter(issue_date__gte=inicio, issue_date__lt=fin)
        #print(licenses)
        context = {
            'licenses':licenses,
        }
        return render(request, "admin/income/licenses/list.html",context)        
    
@login_required
def quotations_view(request):
    return render(request, "admin/income/quotations/index.html")

@login_required
def quotations_list(request):
    if request.method == "POST":
        start = request.POST.get("start_date")
        end = request.POST.get("end_date")
        if start and end:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
            start_date = timezone.make_aware(datetime.combine(start_date, time.min))
            end_date = timezone.make_aware(datetime.combine(end_date, time.max))
            quotations = Quotation.objects.filter(issue_date__range=(start_date, end_date))
            context = { 'quotations':quotations}
            return render(request, "admin/income/quotations/list.html", context) 
        else:
            return HttpResponse("")       
    else:
        # Inicio del día (00:00:00)
        inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # Fin del día siguiente (00:00:00)
        fin = inicio + timedelta(days=1)
        # Consulta de todos los registros del día actual
        quotations = Quotation.objects.filter(issue_date__gte=inicio, issue_date__lt=fin)
        #print(licenses)
        context = {'quotations':quotations}
        return render(request, "admin/income/quotations/list.html",context) 


@login_required
def quotation_customer_search(request):
    if request.method == "POST":
        name_input = request.POST["name"]
        #print("valor: ",type(name_input))
        if name_input != '':
            customers = Customer.objects.annotate(
                nombre_completo=Concat("name",Value(" "),"paternal_surname",Value(" "),"maternal_surname",output_field=CharField(),)
            ).filter(nombre_completo__icontains=name_input)[:10]
            if customers.exists():
                return render(request, "admin/income/quotations/customers_list.html", {"customersList": customers})
            else:
                return render(request, "admin/income/quotations/doesnot_exist_customers.html", {"name": name_input})
        else:
            return HttpResponse('')
    else:
        return render(request, "admin/income/quotations/customer_search.html") 

@login_required
def quotation_new(request,customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    form = QuotationForm(initial={'customer':customer})
    context = {'customer':customer,'form':form}
    return render(request, "admin/income/quotations/new.html",context)   

@login_required
def quotation_save(request):
    if request.method == "POST":
        quotation = QuotationForm(request.POST)
        if quotation.is_valid():
            quotation = quotation.save(commit=False)
            quotation.dependence_id = request.user.profile.dependence.id
            quotation.department_id = request.user.profile.department.id
            quotation.save()
            #items
            concepto_ids = request.POST.getlist("concepto_id[]")
            cantidades = request.POST.getlist("cantidad[]")
            precios = request.POST.getlist("precio[]")    

            for c_id, quantity,unit_price in zip(concepto_ids,cantidades, precios):
                if c_id:  
                    QuotationItem.objects.create(
                        quotation_id=quotation.id,
                        concept_id=c_id,   
                        quantity = float(quantity),
                        unit_price=float(unit_price) or 0,
                    )
            
            context = {'quotation_id':quotation.id}
            return render(request,"admin/income/quotations/success.html",context)
        else:
            customer_id = request.POST["customer"]
            customer = get_object_or_404(Customer, pk=customer_id)
            context = {
                'customer':customer,
                "form":quotation
            }
            return render(request,"admin/income/quotations/new.html",context)

@login_required
def income_quotation_pdf(request,quotation_id, download=False):
    try:
        quotation = Quotation.objects.get(pk=quotation_id)
        items =  quotation.items.all()
        return generate_quotation_pdf(request,quotation,items,download=False)
    except FederalPolicy.DoesNotExist:
        raise Http404("Cotización no encontrada")

@login_required
def income_catalog_view(request):
    return render(request, "admin/income/catalog/index.html")

@login_required
def income_catalog_categories_list(request):
    listCategories = Category.objects.all()
    return render(
        request,
        "admin/income/catalog/category/list.html",
        {"listCategories": listCategories},
    )

@login_required
def income_catalog_category_new(request):
    if request.method == "POST":
        form = catalogCategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "category_form":form                
            }
        return render(request, "admin/payroll/catalog/category/new.html",context)            
    else:
        form = catalogCategoryForm()
        return render(request, "admin/income/catalog/category/new.html", {"category_form": form})
    
@login_required
def income_catalog_category_edit(request, pk):
    model = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = catalogCategoryForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response
    else:
        form = catalogCategoryForm(instance=model)
    return render(
        request,
        "admin/income/catalog/category/edit.html",
        {"form": form, "model": model},
    )

@login_required
def income_catalog_category_delete(request,pk):
    model = get_object_or_404(Category, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/catalog/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/catalog/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateCategoriesList"
        return response    
    return render(request, "admin/income/catalog/category/delete.html", {"model": model})      

@login_required
def income_catalog_subcategories_list(request):
    listSubcategories = Subcategory.objects.all()
    return render(
        request,
        "admin/income/catalog/subcategory/list.html",
        {"listSubcategories": listSubcategories},
    )

@login_required
def income_catalog_subcategory_new(request):
    if request.method == "POST":
        form = catalogSubcategoryForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "UpdateSubcategoriesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "subcategory_form":form                
            }
        return render(request, "admin/payroll/catalog/subcategory/new.html",context)                 
    else:
        form = catalogSubcategoryForm()
        return render(
            request, "admin/income/catalog/subcategory/new.html", {"subcategory_form": form}
        )

@login_required
def income_catalog_subcategory_edit(request, pk):
    model = get_object_or_404(Subcategory, pk=pk)
    if request.method == "POST":
        form = catalogSubcategoryForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/success.html", {"message": message}
            )
            response["HX-Trigger"] = "UpdateSubcategoriesList"
            return response
    else:
        form = catalogSubcategoryForm(instance=model)
    return render(
        request,
        "admin/income/catalog/subcategory/edit.html",
        {"form": form, "model": model},
    )

@login_required
def income_catalog_subcategory_delete(request,pk):
    model = get_object_or_404(Subcategory, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/catalog/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateSubcategoriesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/catalog/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateSubcategoriesList"
        return response    
    return render(request, "admin/income/catalog/subcategory/delete.html", {"model": model})   

@login_required
def income_catalog_concepts_list(request):
    listConcepts = Concept.objects.all()
    return render(
        request,
        "admin/income/catalog/concept/list.html",
        {"listConcepts": listConcepts},
    )

@login_required
def income_catalog_concept_new(request):
    if request.method == "POST":
        form = ConceptForm(request.POST)
        if form.is_valid():
            concept = form.save()
            tax_ids = request.POST.getlist("tax[]")
            print("tax",tax_ids)
            # 3. Recorrer y crear los items
            for tax_id in tax_ids:
                tax_id = int(tax_id)
                if tax_id:  # solo si el concepto tiene un id válido
                    ConceptTax.objects.create(
                        concept_id=concept.id,
                        tax_id=tax_id,   
                    )
            #facturama_concept_new(request,concept)
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/catalog/concept/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateConceptsList"
            return response
        else:
            taxes = Tax.objects.all()
            context = {
                "message":"Existen errores en el formulario",
                "form":form,"taxes":taxes                
            }
            return render(request, "admin/income/catalog/concept/new.html",context)       
    else:
        form = ConceptForm()
        taxes = Tax.objects.all()
        
        #return render(request, "admin/income/catalog/concept/concept_create.html", {"form": form})        
        return render(request, "admin/income/catalog/concept/new.html", {"form": form,"taxes":taxes})

@login_required
def income_catalog_concept_edit(request, pk):
    model = get_object_or_404(Concept, pk=pk)
    if request.method == "POST":
        form = ConceptForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(
                request, "admin/income/catalog/concept/success.html", {"message": message}
            )
            response["HX-Trigger"] = "UpdateConceptsList"
            return response
    else:
        form = ConceptForm(instance=model)
    return render(
        request,
        "admin/income/catalog/concept/edit.html",
        {"form": form, "model": model},
    )

@login_required
def income_catalog_concept_delete(request,pk):
    model = get_object_or_404(Concept, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/catalog/concept/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateConceptsList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/catalog/concept/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateConceptsList"
        return response    
    return render(request, "admin/income/catalog/concept/delete.html", {"model": model})   

#CLIENTES
@login_required
def income_customers_view(request):
    return render(request, "admin/income/customer/index.html")

@login_required
def income_customers_list(request):
    return render(request, "admin/income/customer/list.html")

@require_http_methods(["POST"])
@csrf_exempt
@login_required
def customers_datatable(request):
    """
    Vista AJAX para DataTables con paginación server-side
    Optimizada para manejar grandes volúmenes de datos
    """
    try:
        # Obtener parámetros de DataTables
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        
        # Parámetros de ordenamiento
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_direction = request.POST.get('order[0][dir]', 'asc')
        
        # Mapeo de columnas para ordenamiento
        columns = ['id', 'name','rfc','email','cellphone','phone','acciones']
        order_column = columns[order_column_index] if order_column_index < len(columns) else 'id'
        
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        
        # Query base optimizada con select_related si hay ForeignKeys
        queryset = Customer.objects.all()
        
        # Aplicar filtro de búsqueda si existe
        if search_value:
            queryset = queryset.filter(
                Q(name__icontains=search_value) |
                Q(paternal_surname__icontains=search_value) |
                Q(maternal_surname__icontains=search_value) |
                Q(rfc__icontains=search_value) 
            )
        
        # Contar registros totales y filtrados
        total_records = Customer.objects.count()
        filtered_records = queryset.count()
        
        # Aplicar ordenamiento y paginación
        queryset = queryset.order_by(order_column)[start:start + length]
        data = []
        contador = 1
        for item in queryset:
            data.append({
                'id': contador,
                'name': f"{item.name or ''} {item.paternal_surname or ''} {item.maternal_surname or ''}".strip(),
                'rfc': item.rfc,
                'email':item.email,
                'cellphone':item.cellphone,
                'phone':item.phone,                
                'acciones': f"""
                    <div class="flex space-x-2">
                        <button onclick="CustomerDetail('{item.id}')" 
                                class="text-gray-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button onclick="CustomerEdit('{item.id}')" 
                                class="text-blue-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="CustomerDelete({item.id})" 
                                class="text-red-600 hover:text-red-900 font-medium">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                """
            })
            contador += 1
        
        # Respuesta para DataTables
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        }
        
        return JsonResponse(response)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': []
        }, status=500)

@login_required    
def income_customer_type(request):
    return render(request, "admin/income/customer/customer_type.html")

@login_required    
def income_customer_new(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.employee_id = request.user.id
            customer.save()
            #facturama_customer_new(request,customer)
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/customer/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCustomersList"
            return response
        else:
            message = "Existen errores en el formulario"
            context = {
                'message':message,
                'form':form
            }
            return render(request,"admin/income/customer/new.html",context)                         
    else:
        customer_form = CustomerForm()
    return render(request,"admin/income/customer/new.html",{"form":customer_form})

@login_required
def income_customer_edit(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.employee_id = request.user.id
            customer.save()
            message = "Registro actualizado correctamente"
            response = render(request, "admin/income/customer/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCustomersList"
            return response
        else:
            message = "Existen errores en el formulario"
            context = {
                'message':message,
                'form':form
            }
            return render(request,"admin/income/customer/new.html",context)             
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin/income/customer/edit.html', {'form': form})     


@login_required    
def income_customer_update(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/customer/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCustomersList"
            return response
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin/income/customer/customer_form.html', {'form': form})

@login_required   
def income_customer_save(request):
    if request.method=="POST":
        person_type = int(request.POST["person_type"])
        #print("tipo de persona:",person_type)
        if person_type == 1:
            #print("tipo de persona fisica:",person_type)
            customer_form = personPhysicalForm(request.POST)
            template = "admin/income/customer/person_physical.html"
        if person_type == 2:
            #print("tipo de persona moral:",person_type)
            customer_form = personMoralForm(request.POST)
            template = "admin/income/customer/person_moral.html"
        if customer_form.is_valid():
            customer_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/customer/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCustomersList"
            return response            
        else:
            return render(request,template,{"form":customer_form})
    else:
        return HttpResponse("")           

@login_required
def income_customer_detail(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "admin/income/customer/detail.html",{"customer":customer})



@login_required
def income_customer_delete(request,pk):
    model = get_object_or_404(Customer, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/customer/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateCustomersList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/customer/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateCustomersList"
        return response    
    return render(request, "admin/income/customer/delete.html", {"model": model}) 

# CUENTAS Y BANCOS
@login_required
def income_bank_accounts_view(request):
    return render(request, "admin/income/bank_accounts/index.html")
#bancos
@login_required
def income_banks_list(request):
    banks = Bank.objects.all()
    return render(request, "admin/income/bank_accounts/banks/list.html",{"banks":banks})

@login_required
def income_bank_new(request):
    if request.method == "POST":
        form = BankForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/bank_accounts/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateBanksList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/bank_accounts/banks/new.html",context)       
    else:
        form = BankForm()
        return render(request, "admin/income/bank_accounts/banks/new.html", {"bank_form": form})    

@login_required
def income_bank_detail(request):
    return render(request, "admin/income/bank_accounts/banks/detail.html")

@login_required
def income_bank_edit(request,pk):
    model = get_object_or_404(Bank, pk=pk)
    if request.method == "POST":
        form = BankForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            form.save()
            message = "Registro editado correctamente"
            response = render(request, "admin/income/bank_accounts/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateBanksList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/bank_accounts/banks/edit.html",context)         
    else:
        form = BankForm(instance=model)
    return render(request,"admin/income/bank_accounts/banks/edit.html",{"bank_form": form, "model": model})    

@login_required
def income_bank_delete(request,pk):
    model = get_object_or_404(Bank, pk=pk)
    if request.method == "DELETE":
        print("llego a eliminar banco")
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/bank_accounts/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateBanksList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/bank_accounts/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateBanksList"
        return response    

    return render(request, "admin/income/bank_accounts/banks/delete.html", {"model": model})   

#cuentas 
@login_required
def income_accounts_list(request):
    accounts = BankAccount.objects.all()
    return render(request, "admin/income/bank_accounts/accounts/list.html",{"accounts":accounts})

@login_required
def income_account_new(request):
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/bank_accounts/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateAccountsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/bank_accounts/accounts/new.html",context)       
    else:
        form = AccountForm()
        return render(request, "admin/income/bank_accounts/accounts/new.html", {"account_form": form})        

@login_required
def income_account_detail(request):
    return render(request, "admin/income/bank_accounts/accounts/detail.html")

@login_required
def income_account_edit(request,pk):
    model = get_object_or_404(BankAccount, pk=pk)
    if request.method == "POST":
        form = AccountForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            form.save()
            message = "Registro editado correctamente"
            response = render(request, "admin/income/bank_accounts/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateAccountsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/bank_accounts/accounts/edit.html",context) 
    else:
        form = AccountForm(instance=model)
    return render(request,"admin/income/bank_accounts/accounts/edit.html",{"account_form": form, "model": model})   

@login_required
def income_account_delete(request,pk):
    model = get_object_or_404(BankAccount, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/bank_accounts/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateAccountsList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/bank_accounts/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdateAccountsList"
        return response    
    return render(request, "admin/income/bank_accounts/accounts/delete.html", {"model": model})  

# PREDIAL
@login_required
def income_predial_view(request):
    return render(request, "admin/income/predial/index.html")

@login_required
def income_predial_list(request):
    predial_list = Predial.objects.all()
    return render(request, "admin/income/predial/list.html",{"predial_list":predial_list})

@login_required
def income_predial_new(request):
    if request.method == "POST":
        form = PredialForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/predial/success.html", {"message": message})
            response["HX-Trigger"] = "UpdatePredialList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/predial/new.html",context)       
    else:
        form = PredialForm()
        return render(request, "admin/income/predial/new.html", {"predial_form": form})

@login_required
def income_predial_detail(request):
    return render(request, "admin/income/predial/detail.html")

@login_required
def income_predial_edit(request,pk):
    model = get_object_or_404(Predial, pk=pk)
    if request.method == "POST":
        form = PredialForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            form.save()
            message = "Registro editado correctamente"
            response = render(request, "admin/income/predial/success.html", {"message": message})
            response["HX-Trigger"] = "UpdatePredialList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "form":form                
            }
        return render(request, "admin/income/bank_accounts/predial/edit.html",context)         
    else:
        form = PredialForm(instance=model)
    return render(request,"admin/income/predial/edit.html",{"predial_form": form, "model": model})  

@login_required
def income_predial_delete(request,pk):
    model = get_object_or_404(Predial, pk=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/predial/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdatePredialList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except model.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/predial/error.html",{"message": message},)
        response["HX-Trigger"] = "UpdatePredialList"
        return response    
    return render(request, "admin/income/predial/delete.html", {"model": model})  

# REPORTES
@login_required
def income_reports_view(request):
    return render(request, "admin/income/reports/index.html")

@login_required
def income_reports_list(request):
    employees  = Profile.objects.filter(dependence_id = 3,department_id=3)
    print(employees)
    return render(request, "admin/income/reports/ListOfReports.html",{"employees":employees})

@login_required
def income_reports_types(request):
    if request.method == "GET":
        report_type = request.GET.get('report_type')
        valid_reports = ['customer', 'invoice', 'dates', 'category', 'subcategory', 'concept']
        if report_type in valid_reports:
            if report_type == 'category':
                data = Category.objects.all()
                template_path = f"admin/income/reports/partials/{report_type}.html"
                context = {"data":data}
                return render(request, template_path, context)
            if report_type == 'subcategory':
                data = Subcategory.objects.all()
                template_path = f"admin/income/reports/partials/{report_type}.html"
                context = {"data":data}
                return render(request, template_path, context)       
            if report_type == 'concept':
                data = Concept.objects.all()
                template_path = f"admin/income/reports/partials/{report_type}.html"
                context = {"data":data}
                return render(request, template_path, context)                         
            else:
                template_path = f"admin/income/reports/partials/{report_type}.html"
                return render(request, template_path)
        else:
            return HttpResponseNotFound("Tipo de reporte no válido")                                    

# --- Funciones de consulta (lógica de negocio) ---
def get_daily_incomes():
    return Invoice.objects.filter(issue_date__date=timezone.now().date()).order_by('issue_date')

def get_incomes_by_customer(customer_name):
    # Aquí se utiliza la variable 'customer_name' para filtrar
    return Customer.objects.annotate(
                nombre_completo=Concat("name",Value(" "),"paternal_surname",Value(" "),"maternal_surname",output_field=CharField(),)
            ).filter(nombre_completo__icontains=customer_name)[:10]    
    #return Customer.objects.filter(customer__name=customer_name)

def get_incomes_by_customerid(customer_id):
    return Invoice.objects.filter(customer_id=customer_id)

def get_incomes_by_dates(start_date, end_date):
    # Asegúrate de que las fechas se pasen como objetos de fecha de Python
    return Invoice.objects.filter(issue_date__range=(start_date, end_date))

def get_incomes_by_invoice(start_date, end_date):
    # Asegúrate de que las fechas se pasen como objetos de fecha de Python
    return Invoice.objects.filter(issue_date__range=(start_date, end_date),invoice=True)

def get_incomes_by_category(category_no, start_date, end_date):
    # Asegúrate de que las fechas se pasen como objetos de fecha de Python
    return Invoice.objects.filter(issue_date__range=(start_date, end_date),items__concept__category__account_number=category_no).distinct()

def get_incomes_by_subcategory(subcategory_no, start_date, end_date):
    # Asegúrate de que las fechas se pasen como objetos de fecha de Python
    return Invoice.objects.filter(issue_date__range=(start_date, end_date),items__concept__subcategory__account_number=subcategory_no).distinct()

def get_incomes_by_concept(concept_no, start_date, end_date):
    # Asegúrate de que las fechas se pasen como objetos de fecha de Python
    return Invoice.objects.filter(issue_date__range=(start_date, end_date),items__concept__account_number=concept_no).distinct()

@login_required
def income_reports_search(request):
    query_functions = {
        'daily': get_daily_incomes,
        'customer': get_incomes_by_customer,
        'customerid': get_incomes_by_customerid,
        'dates': get_incomes_by_dates,
        'invoice':get_incomes_by_invoice,
        'category':get_incomes_by_category,
        'subcategory':get_incomes_by_subcategory,
        'concept':get_incomes_by_concept,
    }
    report_type = request.POST.get('report_type')
    query_func = query_functions.get(report_type)
    if not query_func:
        return HttpResponseNotFound("Tipo de reporte no válido")
    # Obtener los parámetros de la URL usando request.GET
    customer_name = request.POST.get('customer_name')
    customer_id = request.POST.get('customer_id')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    category_no = request.POST.get('category_no')
    subcategory_no = request.POST.get('subcategory_no')
    concept_no = request.POST.get('concept_no')
    # Convertir las variables según sea necesario
    #start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    # end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    if start_date and end_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        # Crear rango de todo el día (00:00:00 a 23:59:59)
        start_date = timezone.make_aware(datetime.combine(start_date, time.min))
        end_date = timezone.make_aware(datetime.combine(end_date, time.max))
    # Llama a la función de consulta con los argumentos correctos
    try:
        if report_type == 'customer' and customer_name:
            data = query_func(customer_name)
        elif report_type == 'customerid' and customer_id:
            data = query_func(customer_id)            
        elif report_type == 'dates' and start_date and end_date:
            data = query_func(start_date, end_date)
        elif report_type == 'invoice' and start_date and end_date:
            data = query_func(start_date, end_date)     
        elif report_type == 'category' and start_date and end_date and category_no:
            data = query_func(category_no, start_date, end_date)
        elif report_type == 'subcategory' and start_date and end_date and subcategory_no:
            data = query_func(subcategory_no, start_date, end_date)  
        elif report_type == 'concept' and start_date and end_date and concept_no:
            data = query_func(concept_no, start_date, end_date)                                               
        elif report_type == 'daily':
            data = query_func()
        else:
            # Manejar el caso de parámetros faltantes
            #return HttpResponseNotFound("Faltan parámetros para el reporte.")
            return HttpResponse("")
    except Exception as e:
        # Manejo de errores en la consulta, como formato de fecha incorrecto
        return HttpResponseNotFound(f"Error en la consulta: {e}")

    template_path = f"admin/income/reports/{report_type}.html"
    context = {'report_data': data, 'report_type': report_type}
    return render(request, template_path, context)

#TODO: POLIZAS
@login_required
def income_policy_view(request):
    return render(request, "admin/income/policy/index.html")

#? POLIZA DE CAJA
@login_required
def income_cash_policy_list(request):
    cash_policy = CashPolicy.objects.all()
    return render(request,"admin/income/policy/cash/list.html", {"cash_policy":cash_policy})

@login_required
def cash_policy(request):
    return render(request,"admin/income/policy/cash/index.html")

@login_required
def income_cash_policy_new(request):
    if request.method == "POST":
        cash_policy_form = CashPolicyForm(request.POST)
        if cash_policy_form.is_valid():
            #guarda poliza
            my_policy = cash_policy_form.save()
            #Obtenemos variables
            conceptos_ids = request.POST.getlist("concepto_id[]")
            importes = request.POST.getlist("predial_amount[]")
            cash_register = request.POST.getlist("cash_register[]")
            start_receipt = request.POST.getlist("start[]")
            end_receipt = request.POST.getlist("end[]")
            #Guarda los importes de predial
            for c_id,importe in zip(conceptos_ids,importes):
                if c_id:
                    PolicyPredialItem.objects.create(
                        policy_id = my_policy.id,
                        concept_id = c_id,
                        amount = float(importe) or 0,
                    )   
            #Guarda los numeros de recibos utilizados
            for caja,recibo_inicio,recibo_fin in zip(cash_register,start_receipt,end_receipt):
                if caja and recibo_inicio != '' and recibo_fin != '':
                    CashPolicyReceipt.objects.create(
                        policy_id = my_policy.id,
                        cash_register_id = caja,
                        start_receipt = recibo_inicio,
                        end_receipt = recibo_fin
                    )
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/policy/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCashPolicyList"
            return response
    if request.method == "GET":
        #Recibo fecha y aplico formato
        current_date = request.GET.get('date')
        if current_date:
            date = datetime.strptime(current_date, "%Y-%m-%d").date()
            #? Crear rango de todo el día (00:00:00 a 23:59:59)
            start_date = timezone.make_aware(datetime.combine(date, time.min))
            end_date = timezone.make_aware(datetime.combine(date, time.max))
            #?Listado de conceptos de caja
            cash_concepts=InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="caja").filter(concept__predial=False).values('concept__id','concept__account_number','concept__name').annotate(total=Sum('total')).order_by('concept__account_number')
            if cash_concepts.exists():
                #print("La consulta devolvió registros.")
                #?Obtengo el total acomulado de las facturas
                #sum_total_amount = Invoice.objects.filter(issue_date__range=(start_date, end_date)).aggregate(total=Sum('total_amount'))  
                #invoice_total = sum_total_amount['total']
                #print("Total en facturas:", invoice_total)
                #?total de caja
                total_sum_cash = InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="caja").filter(concept__predial=False).aggregate(total_price=Sum('total'))
                cash_concepts_total = total_sum_cash['total_price']
                #print("Total en InvoiceItems:", cash_concepts_total)
                #?Recibos de caja
                min_id = Invoice.objects.filter(issue_date__range=(start_date, end_date)).aggregate(min_id=Min('id'))['min_id']
                max_id = Invoice.objects.filter(issue_date__range=(start_date, end_date)).aggregate(max_id=Max('id'))['max_id']         
                #?Otras cajas (para registrar sus recibos) 
                cash_registers = CashRegister.objects.all()
                #formulario de caja
                cash_policy_form = CashPolicyForm()
                context = {
                    'date':current_date,
                    #'total_amount':sum_total_amount['total'],
                    'list_cash_concepts':cash_concepts,
                    'total_cash_concepts': cash_concepts_total,
                    #'predial_concepts':predial_concepts,
                    'cash_receipt_min':min_id,
                    'cash_receipt_max':max_id,
                    'cash_policy_form':cash_policy_form,
                    'cash_registers':cash_registers
                }
                return render(request,"admin/income/policy/cash/new.html",context)              
        else:
            #print("La consulta no devolvió registros.")
            return render(request,"admin/income/policy/not_found.html",)


@login_required
def cash_policy_pdf(request,policy_id, download=False):
    try:
        policy = CashPolicy.objects.get(pk=policy_id)
        date = policy.date
        start_date = timezone.make_aware(datetime.combine(date, time.min))
        end_date = timezone.make_aware(datetime.combine(date, time.max))        
        #print("fecha:",date)
        #?Listado de conceptos de caja
        cash_concepts=InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="caja").filter(concept__predial=False).values('concept__account_number','concept__name').annotate(total=Sum('total')).order_by('concept__account_number')
        #print("Conceptos de poliza:",cash_concepts)
        concepts_predial=policy.items_predial.all()
        #print("Conceptos de predial:",concepts_predial)
        #for item  in concepts_predial:
        #    print("concepto",item.concept.name)
        #    print("monto",item.amount)
        #?Recibos de caja
        receipts =  policy.items_receipts.all()
        #print("Recibos:",receipts)
        name_izq = "Elaboró: " + policy.prepare
        name_der = "Revisó: " + policy.review
        #return HttpResponse("")
        return generate_cash_policy_pdf(request,policy,cash_concepts,concepts_predial,receipts,name_izq,name_der,download=False)
    except CashPolicy.DoesNotExist:
        raise Http404("Poliza no encontrada")

@login_required 
def cash_policy_delete(request,pk):
    model = get_object_or_404(CashPolicy, pk=pk)
    if request.method == "DELETE":
        model.delete()
        message = "Registro eliminado correctamente"
        response = render(request,"admin/income/policy/success.html",{"message": message},)
        response["HX-Trigger"] = "UpdateCashPolicyList"
        return response           
    else:
        return render(request,"admin/income/policy/cash/delete.html",{'model':model})


#? POLIZA FEDERAL
@login_required
def income_federal_policy_list(request):
    federal_policy = FederalPolicy.objects.all()
    return render(request,"admin/income/policy/federal/list.html",{"federal_policy":federal_policy})

@login_required
def federal_policy(request):
    return render(request,"admin/income/policy/federal/index.html")

@login_required
def income_federal_policy_new(request):
    if request.method == "POST":
        federal_policy_form = FederalPolicyForm(request.POST)
        if federal_policy_form.is_valid():
            my_policy = federal_policy_form.save()
            concepts = request.POST.getlist("concept[]")
            accounts_banks = request.POST.getlist("account_bank[]")
            amounts = request.POST.getlist("amount[]")
            #print("conceptos",concepts)
            #print("cuentas",accounts_banks)
            #print("importes",amounts)
            #Recorre item para guardar recibos
            for concept,account_bank,amount in zip(concepts,accounts_banks,amounts):
                if concept:
                    FederalPolicyItem.objects.create(
                        policy_id = my_policy.id,
                        concept_id = concept,
                        bank_account_id = account_bank,
                        amount = float(amount) or 0
                    )
            message = "Registro realizado correctamente"
            response = render(request, "admin/income/policy/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateFederalPolicyList"
            return response
    if request.method == "GET":
        fecha = request.GET.get('date')
        if fecha:
            date = datetime.strptime(fecha, '%Y-%m-%d').date()
            #? Crear rango de todo el día (00:00:00 a 23:59:59)
            start_date = timezone.make_aware(datetime.combine(date, time.min))
            end_date = timezone.make_aware(datetime.combine(date, time.max))                             
            #? Listado de conceptos de caja
            list_federal_concepts=InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="federal").values('concept__id','concept__account_number','concept__name').annotate(total=Sum('total')).order_by('concept__account_number')
            #total de caja
            total_sum_federal = InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="federal").aggregate(total_price=Sum('total'))
            federal_concepts_total = total_sum_federal['total_price']
            #Recibos de caja
            #min_id = Receipt.objects.aggregate(min_id=Min('id'))['min_id']
            #max_id = Receipt.objects.aggregate(max_id=Max('id'))['max_id']           
            federal_policy_form = FederalPolicyForm()
            accounts_banks=BankAccount.objects.all()
            context = {
                'date':fecha,
                'list_federal_concepts':list_federal_concepts,
                'total_federal_concepts': federal_concepts_total,
                #'predial_concepts':predial_concepts,
                #'cash_receipt_min':min_id,
                #'cash_receipt_max':max_id,
                'federal_policy_form':federal_policy_form,
                #'cash_registers':cash_registers
                'accounts_banks':accounts_banks,
            }        
            return render(request,"admin/income/policy/federal/new.html",context)

@login_required 
def federal_policy_delete(request,pk):
    print("id de poliza",pk)
    model = get_object_or_404(FederalPolicy, pk=pk)
    if request.method == "DELETE":
        model.delete()
        message = "Registro eliminado correctamente"
        response = render(request,"admin/income/policy/success.html",{"message": message},)
        response["HX-Trigger"] = "UpdateFederalPolicyList"
        return response           
    else:
        return render(request,"admin/income/policy/federal/delete.html",{'model':model})

@login_required
def income_policy_concept_search(request):
    q = request.GET.get("q", "")
    conceptos = Concept.objects.filter(name__icontains=q, predial=True).values("id", "name", "account_number")[:10]
    return JsonResponse(list(conceptos), safe=False)

@login_required
def federal_policy_pdf(request,policy_id, download=False):
    try:
        policy = FederalPolicy.objects.get(pk=policy_id)
        date = policy.date
        start_date = timezone.make_aware(datetime.combine(date, time.min))
        end_date = timezone.make_aware(datetime.combine(date, time.max))                
        concepts=InvoiceItem.objects.filter(invoice__issue_date__range=(start_date, end_date)).filter(concept__subcategory__category__income_type="federal").values('concept__id','concept__account_number','concept__name').annotate(total=Sum('total')).order_by('concept__account_number')
        #print(concepts)
        items =  policy.items_federal.all()
        name_izq = "Elaboró: " + policy.prepare
        name_der = "Revisó: " + policy.review
        return generate_federal_policy_pdf(request,policy,concepts,items,name_izq,name_der,download=False)
    except FederalPolicy.DoesNotExist:
        raise Http404("Poliza no encontrada")
    
@login_required
def concepts_view(request):
    conceptos = Concept.objects.all().filter(online_payment = True)
    #print(products)
    cart_count = 0
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_count = cart.items.count()
    
    return render(request, 'admin/payments/index.html', {
        'concepts': conceptos,
        'cart_count': cart_count
    })

@login_required
def payment_concept_search(request):
    q = request.GET.get("concept", "")
    conceptos = Concept.objects.filter(online_payment = True).filter(name__icontains=q)
    return render(request, 'admin/payments/concepts.html',{'concepts':conceptos})

@login_required
@require_POST
def add_to_cart(request, concept_id):
    concept = get_object_or_404(Concept, id=concept_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    quantity = int(request.POST.get('quantity', 1))
    
    #if concept.stock >= quantity:
    cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            concept=concept,
            defaults={'quantity': quantity}
        )
        
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
        
    messages.success(request, f'{concept.name} agregado al carrito')
    #else:
    #    messages.error(request, 'Stock insuficiente')
    
    return redirect('income:concepts_view')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('concept').all()
    
    total = sum(item.get_total_price() for item in cart_items)
    
    return render(request, 'admin/payments/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

@login_required
@require_POST
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    action = request.POST.get('action')
    
    if action == 'increase':
        #if cart_item.product.stock > cart_item.quantity:
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    elif action == 'remove':
        cart_item.delete()
    
    return redirect('income:view_cart')

@login_required
def payment_customer_data(request):
    if request.method == 'GET':
        customer, _ = Customer.objects.get_or_create(user=request.user)
        form = CustomerForm(instance=customer)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.select_related('concept').all()
        total = sum(item.get_total_price() for item in cart_items)
        context = {
            'form':form,
            'customer':customer,
            'cart_items':cart_items,
            'total':total,
        }
        return render(request, "admin/payments/customer.html",context)
    
@login_required
def person_physical(request):
    return render(request,"admin/income/customer/physical_person.html")

@login_required
def person_moral(request):
    return render(request,"admin/income/customer/moral_person.html")

@login_required
def create_checkout_session(request):
    print("llego al checkout")
    customer = get_object_or_404(Customer, user_id=request.user)
    customer_form = CustomerForm(request.POST, instance=customer)
    if customer_form.is_valid():
        print("formulario de cliente valido")
        customer_form.save()
    else:
        print("formulario invalido",customer_form.errors)
        messages.error(request, 'Verifica tus datos')
        return redirect('income:customer_data')

    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.items.select_related('concept').all()
    print("productos en el carrito")
    print(cart_items)
    if not cart_items:
        print("Tu carrrito está vacio")
        messages.error(request, 'Tu carrito está vacío')
        return redirect('income:view_cart')
    
    # Verificar stock
    #for item in cart_items:
    #    if item.product.stock < item.quantity:
    #        messages.error(request, f'Stock insuficiente para {item.product.name}')
    #        return redirect('income:view_cart')
    
    try:
        line_items = []
        total_amount = 0
        
        for item in cart_items:
            line_items.append({
                'price_data': {
                    'currency': 'mxn',  # o 'mxn'
                    'product_data': {
                        'name': item.concept.name,
                        #'description': item.concept.description,
                    },
                    'unit_amount': int(item.concept.unit_price * 100),
                },
                'quantity': item.quantity,
            })
            total_amount += item.get_total_price()
            print("El total acoumlado:",total_amount)
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
            customer_email=request.user.email,
            metadata={
                'cart_id': str(cart.id),
                'user_id': str(request.user.id),
                'total_amount': str(total_amount),
                #'invoice': cart.invoice
            }
        )
        # Guardar el session_id en la sesión de Django
        request.session['stripe_session_id'] = checkout_session.id
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(str(e))
        messages.error(request, f'Error al procesar el pago: {str(e)}')
        return redirect('income:view_cart')

def payment_success(request):
    print("llegue a success")
    stripe_session_id = request.session.get('stripe_session_id')
    
    if stripe_session_id:
        try:
            session = stripe.checkout.Session.retrieve(stripe_session_id)
            payment = Invoice.objects.filter(stripe_payment_intent_id=session.payment_intent).first()
            
            # Limpiar la sesión
            del request.session['stripe_session_id']
            
            return render(request, 'admin/payments/pay_success.html', {'payment': payment})
        except:
            pass    
    return render(request, 'admin/payments/pay_success.html')

def payment_cancel(request):
    print("llegue a cancel")
    return render(request, 'admin/payments/pay_cancel.html')

@csrf_exempt
def stripe_webhook(request):
    print("stripe_webhook")
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        process_successful_payment(session)

    return HttpResponse(status=200)

def process_successful_payment(session):
    print("llegue a process_successful_payment")
    """Procesa un pago exitoso y genera el recibo"""
    try:
        cart_id = session['metadata']['cart_id']
        user_id = session['metadata']['user_id']
        total_amount = Decimal(session['metadata']['total_amount'])
        #require_invoice = session['metadata']['invoice']
        
        cart = Cart.objects.get(id=cart_id)
        #user = cart.user
        customer = get_object_or_404(Customer, user=user_id)
        # Crear el registro de pago
        payment = Invoice.objects.create(
            customer_id=customer.id,
            pay_form_id = 'stripe',
            invoice = 'False',
            #currency = 'MXN',
            stripe_payment_intent_id=session['payment_intent'],
            total_amount= total_amount,
            paid_amount = total_amount,
            payment_method_id = 'PUE',
            payment_status_id = 'pagado',
            issue_date = timezone.now(),
            #customer_email=session['customer_details']['email'] or user.email,
        )
        
        # Crear items del pago y actualizar stock
        for cart_item in cart.items.all():
            InvoiceItem.objects.create(
                invoice_id=payment.id,
                concept_id=cart_item.concept.id,
                quantity=float(cart_item.quantity),
                unit_price=float(cart_item.concept.unit_price),
            )
            
            # Actualizar stock
            #cart_item.product.stock -= cart_item.quantity
            print("cart_item ->")
            print(cart_item.concept)
            cart_item.concept.save()
        
        # Generar PDF
        #pdf_path = generate_pdf_receipt(payment)
        
        # Enviar email con PDF
        #send_receipt_email(payment, pdf_path)
        
        # Limpiar carrito
        cart.items.all().delete()
        cart.delete()
        #carrito = get_object_or_404(Cart, pk=cart_id)
        #carrito.delete()
        print("se limpio el carrito")
        
    except Exception as e:
        print(f"Error processing payment: {str(e)}")

def send_receipt_email(payment, pdf_path):
    """Envía el recibo por email"""
    try:
        subject = f'Recibo de Compra - {payment.id}'
        
        html_message = render_to_string('admin/payments/email_receipt.html', {
            'payment': payment,
            'user': payment.user,
        })
        
        email = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[payment.user.email],
        )
        email.content_subtype = 'html'
        
        # Adjuntar PDF
        if pdf_path:
            email.attach_file(pdf_path)
        
        email.send()
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")

#TODO: CONFIGURACIÓN
@login_required
def configuration_view(request):
    return render(request,"admin/income/configuration/index.html")
#? COLONIAS
@login_required
def colonies_list(request):
    colonies = Colony.objects.all()
    return render(request,"admin/income/configuration/colonies/list.html",{'colonies':colonies})

@login_required
def colony_new(request):
    if request.method == 'POST':
        form = ColonyForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateColoniesList"
            return response             
    else:
        form = ColonyForm()
    return render(request,"admin/income/configuration/colonies/new.html",{'form':form})

@login_required
def colony_edit(request,pk):
    colony = get_object_or_404(Colony, pk=pk)
    if request.method == 'POST':
        form = ColonyForm(request.POST, instance=colony)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateColoniesList"
            return response 
    else:
        form = ColonyForm(instance=colony)
    return render(request, 'admin/income/configuration/colonies/edit.html', {'form': form})

@login_required
def colony_delete(request,pk):
    colony = get_object_or_404(Colony, pk=pk)
    if request.method == 'DELETE':
        try:
            colony.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateColoniesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except colony.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/colonies/error.html",{"message": message})
        response["HX-Trigger"] = "UpdateColoniesList"
        return response
    else:
        return render(request, "admin/income/configuration/colonies/delete.html", {"colony": colony})                     

#? CAJAS REGISTRADORAS
@login_required
def cash_registers_list(request):
    cash_registers = CashRegister.objects.all()
    return render(request,"admin/income/configuration/cash_registers/list.html",{'cash_registers':cash_registers})

@login_required
def cash_register_new(request):
    if request.method == 'POST':
        form = CashRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateCashRegistersList"
            return response             
    else:
        form = CashRegisterForm()
    return render(request,"admin/income/configuration/cash_registers/new.html",{'form':form})

@login_required
def cash_register_edit(request,pk):
    cash_register = get_object_or_404(CashRegister, pk=pk)
    if request.method == 'POST':
        form = CashRegisterForm(request.POST, instance=cash_register)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateCashRegistersList"
            return response 
    else:
        form = CashRegisterForm(instance=cash_register)
    return render(request, 'admin/income/configuration/cash_registers/edit.html', {'form': form})

@login_required
def cash_register_delete(request,pk):
    cash_register = get_object_or_404(CashRegister, pk=pk)
    if request.method == 'DELETE':
        try:
            cash_register.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateCashRegistersList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except cash_register.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/cash_registers/error.html",{"message": message})
        response["HX-Trigger"] = "UpdateCashRegistersList"
        return response
    else:
        return render(request, "admin/income/configuration/cash_registers/delete.html", {"cash_register": cash_register})                     

#? TIPOS DE INGRESOS
@login_required
def income_types_list(request):
    income_types = IncomeType.objects.all()
    return render(request,"admin/income/configuration/income_types/list.html",{'income_types':income_types})

@login_required
def income_type_new(request):
    if request.method == 'POST':
        form = IncomeTypeForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateIncomeTypesList"
            return response             
    else:
        form = IncomeTypeForm()
    return render(request,"admin/income/configuration/income_types/new.html",{'form':form})

@login_required
def income_type_edit(request,pk):
    income_type = get_object_or_404(IncomeType, pk=pk)
    if request.method == 'POST':
        form = IncomeTypeForm(request.POST, instance=income_type)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateIncomeTypesList"
            return response 
    else:
        form = IncomeTypeForm(instance=income_type)
    return render(request, 'admin/income/configuration/income_types/edit.html', {'form': form})

@login_required
def income_type_delete(request,pk):
    income_type = get_object_or_404(IncomeType, pk=pk)
    if request.method == 'DELETE':
        try:
            income_type.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateIncomeTypesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except income_type.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/income_types/error.html",{"message": message})
        response["HX-Trigger"] = "UpdateIncomeTypesList"
        return response
    else:
        return render(request, "admin/income/configuration/income_types/delete.html", {"income_type": income_type})                     

#? FORMAS DE PAGO
@login_required
def payment_forms_list(request):
    payment_forms = PaymentForm.objects.all()
    return render(request,"admin/income/configuration/payment_forms/list.html",{'payment_forms':payment_forms})

@login_required
def payment_form_new(request):
    if request.method == 'POST':
        form = PaymentForm_Form(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentFormsList"
            return response             
    else:
        form = PaymentForm_Form()
    return render(request,"admin/income/configuration/payment_forms/new.html",{'form':form})

@login_required
def payment_form_edit(request,pk):
    payment_form = get_object_or_404(PaymentForm, pk=pk)
    if request.method == 'POST':
        form = PaymentForm_Form(request.POST, instance=payment_form)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentFormsList"
            return response 
    else:
        form = PaymentForm_Form(instance=payment_form)
    return render(request, 'admin/income/configuration/payment_forms/edit.html', {'form': form})

@login_required
def payment_form_delete(request,pk):
    payment_form = get_object_or_404(PaymentForm, pk=pk)
    if request.method == 'DELETE':
        try:
            payment_form.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdatePaymentFormsList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except payment_form.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/payment_forms/error.html",{"message": message})
        response["HX-Trigger"] = "UpdatePaymentFormsList"
        return response
    else:
        return render(request, "admin/income/configuration/payment_forms/delete.html", {"payment_form": payment_form})                     

#? METODOS DE PAGO
@login_required
def payment_methods_list(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request,"admin/income/configuration/payment_methods/list.html",{'payment_methods':payment_methods})

@login_required
def payment_method_new(request):
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentMethodsList"
            return response             
    else:
        form = PaymentMethodForm()
    return render(request,"admin/income/configuration/payment_methods/new.html",{'form':form})

@login_required
def payment_method_edit(request,pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentMethodsList"
            return response 
    else:
        form = PaymentMethodForm(instance=payment_method)
    return render(request, 'admin/income/configuration/payment_methods/edit.html', {'form': form})

@login_required
def payment_method_delete(request,pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk)
    if request.method == 'DELETE':
        try:
            payment_method.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdatePaymentMethodsList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except payment_method.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/payment_methods/error.html",{"message": message})
        response["HX-Trigger"] = "UpdatePaymentMethodsList"
        return response
    else:
        return render(request, "admin/income/configuration/payment_methods/delete.html", {"payment_method": payment_method})                     


#? ESTADOS DE PAGO
@login_required
def payment_status_list(request):
    payment_status = PaymentStatus.objects.all()
    return render(request,"admin/income/configuration/payment_status/list.html",{'payment_status':payment_status})

@login_required
def payment_state_new(request):
    if request.method == 'POST':
        form = PaymentStatusForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentStatusList"
            return response             
    else:
        form = PaymentStatusForm()
    return render(request,"admin/income/configuration/payment_status/new.html",{'form':form})

@login_required
def payment_state_edit(request,pk):
    payment_state = get_object_or_404(PaymentStatus, pk=pk)
    if request.method == 'POST':
        form = PaymentStatusForm(request.POST, instance=payment_state)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdatePaymentStatusList"
            return response 
    else:
        form = PaymentStatusForm(instance=payment_state)
    return render(request, 'admin/income/configuration/payment_status/edit.html', {'form': form})

@login_required
def payment_state_delete(request,pk):
    payment_state = get_object_or_404(PaymentStatus, pk=pk)
    if request.method == 'DELETE':
        try:
            payment_state.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdatePaymentStatusList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except payment_state.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/payment_status/error.html",{"message": message})
        response["HX-Trigger"] = "UpdatePaymentStatusList"
        return response
    else:
        return render(request, "admin/income/configuration/payment_status/delete.html", {"payment_state": payment_state})                     

#? MONEDAS
@login_required
def currencies_list(request):
    currencies = Currency.objects.all()
    return render(request,"admin/income/configuration/payment_status/list.html",{'currencies':currencies})

@login_required
def currency_new(request):
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateCurrenciesList"
            return response             
    else:
        form = CurrencyForm()
    return render(request,"admin/income/configuration/currencies/new.html",{'form':form})

@login_required
def currency_edit(request,pk):
    currency = get_object_or_404(PaymentStatus, pk=pk)
    if request.method == 'POST':
        form = CurrencyForm(request.POST, instance=currency)
        if form.is_valid():
            form.save()
            message = "Registro actualizado correctamente"
            response =  render(request,"admin/income/configuration/success.html",{"message": message})
            response["HX-Trigger"] = "UpdateCurrenciesList"
            return response 
    else:
        form = CurrencyForm(instance=currency)
    return render(request, 'admin/income/configuration/currencies/edit.html', {'form': form})

@login_required
def currency_delete(request,pk):
    currency = get_object_or_404(PaymentStatus, pk=pk)
    if request.method == 'DELETE':
        try:
            currency.delete()
            message = "Registro eliminado correctamente"
            response = render(request,"admin/income/configuration/success.html",{"message": message},)
            response["HX-Trigger"] = "UpdateCurrenciesList"
            return response        
        except ProtectedError:
            message = "No se puede eliminar porque tiene relaciones asociadas."
        except IntegrityError:
            message = "Error de integridad: El registro no se puede eliminar."
        except currency.DoesNotExist:
            message = "El registro no existe."
        response = render(request,"admin/income/configuration/currencies/error.html",{"message": message})
        response["HX-Trigger"] = "UpdateCurrenciesList"
        return response
    else:
        return render(request, "admin/income/configuration/currencies/delete.html", {"currency": currency})                     

