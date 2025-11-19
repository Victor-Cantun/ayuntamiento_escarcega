from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
#from datetime import datetime
from apps.core.models import dependence, department
from django.core.validators import RegexValidator

# Create your models here.
class Colony(models.Model):
    TYPE_CHOICES = [
        ('colonia', 'Colonia'),
        ('ejido',  'Ejido'),
        ('rancheria',  'Ranchería'),
        ('pueblo',  'Pueblo'),
        ('fraccionamiento',  'Fraccionamiento'),
    ]
    ZONE_CHOICES = [
        ('urbana', 'Urbana'),
        ('rural',  'Rural'),
    ]
    id=models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Colonia:", max_length=150)
    type = models.CharField(verbose_name="Tipo", max_length=30, choices=TYPE_CHOICES, default='colonia') 
    postal_code =  models.CharField(verbose_name="Código postal:", max_length=10,null=True, blank=True,)
    municipality = models.CharField(verbose_name="Municipio:", default='Escárcega')
    city = models.CharField(verbose_name="Ciudad:", null=True, blank=True)
    zone = models.CharField(verbose_name="Zona:", max_length=20, choices=ZONE_CHOICES, default='urbana')

    def __str__(self):
        return self.name

class FiscalRegimen(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(verbose_name="Código:", max_length=150)
    description = models.CharField(verbose_name="Descripción:", max_length=500)   

    def __str__(self):
        return f"{self.code} - {self.description}"

class CfdiUse(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(verbose_name="Código:", max_length=150)
    description = models.CharField(verbose_name="Descripción:", max_length=500)
    fisica = models.BooleanField(verbose_name="Aplica a persona física:")          
    moral = models.BooleanField(verbose_name="Aplica a persona física:")
    regimen_fiscal  = models.TextField(verbose_name="Régimen fiscal:")

    def __str__(self):
        return f"{self.code} - {self.description}"    

class UnitCode(models.Model):
    uso_CHOICES = [
        ('Producto', 'Producto'),
        ('Servicio',  'Servicio'),
    ]    
    id=models.AutoField(primary_key=True)
    uso = models.CharField(verbose_name="Uso:", max_length=20, choices=uso_CHOICES)
    unidad_medida = models.CharField(verbose_name="Unidad de medida SAT:", max_length=20)
    clave_sat = models.CharField(verbose_name="Clave SAT:", max_length=20)
    descripcion = models.TextField(verbose_name="¿Cuándo se utiliza?")

    def __str__(self):
        return f"{self.clave_sat} - {self.unidad_medida}" 

class Tax(models.Model):
    TAX_CODES = [
        ("001", "ISR"),
        ("002", "IVA"),
        ("003", "IEPS"),
    ]

    FACTOR_TYPES = [
        ("Tasa", "Tasa"),
        ("Cuota", "Cuota"),
        ("Exento", "Exento"),
    ]    
    id = models.AutoField(primary_key=True)      
    name = models.CharField(verbose_name="Nombre del Impuesto:", max_length=50)
    rate = models.DecimalField(verbose_name="Tarifa:",max_digits=10, decimal_places=6, default=0.000000)#impuesto
    IsRetention = models.BooleanField(verbose_name="Es Retenido:", default=False)
    IsFederalTax = models.BooleanField(verbose_name="Es Impuesto Federal:", default=True)
    IsQuota = models.BooleanField(verbose_name="Es cuota:", default=False)
    Total = models.DecimalField(verbose_name="Total:",max_digits=10, decimal_places=2, default=0.00)#Total

    sat_tax_code = models.CharField(
        "Código SAT",
        max_length=3,
        choices=TAX_CODES,
        null=True, blank=True
    )

    factor_type = models.CharField(
        "Tipo de Factor",
        max_length=10,
        choices=FACTOR_TYPES,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} - {self.rate}" 

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer')
    person_types = [(1, "Persona física"), (2, "Persona moral")]
    person_type = models.IntegerField(verbose_name="Tipo de contribuyente:", choices=person_types, default=1)
    rfc = models.CharField(verbose_name="RFC", max_length=13, validators=[RegexValidator(r'^[A-Z&Ñ]{3,4}\d{6}[A-V1-9][A-Z1-9][0-9A]$')], unique=True, null=True, blank=True)
    name = models.CharField(verbose_name="Nombre:", max_length=100) #requerido
    paternal_surname = models.CharField(verbose_name="Primer apellido:", max_length=50, null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Segundo apellido:", max_length=50, null=True, blank=True)
    country = models.CharField(verbose_name="Pais:", null=True, blank=True, default='MÉXICO')
    state = models.CharField(verbose_name="Estado:", null=True, blank=True, default='CAMPECHE')
    municipality = models.CharField(verbose_name="Municipio:", null=True, blank=True, default='ESCÁRCEGA')
    colony = models.ForeignKey(Colony, verbose_name="Colonia:", on_delete=models.SET_NULL, null=True, blank=True) #Neighborhood
    postal_code = models.CharField(verbose_name="Código postal:", null=True, blank=True)#requerido
    street = models.CharField(verbose_name="Calle:", max_length=200)
    no_ext = models.CharField(verbose_name="No.Ext:", max_length=10, null=True, blank=True)
    no_int = models.CharField(verbose_name="No.Int:", max_length=10, null=True, blank=True)
    reference = models.CharField(verbose_name="Referencia:", null=True, blank=True)
    cellphone = models.CharField(verbose_name="Celular:", null=True, blank=True)
    phone = models.CharField(verbose_name="Teléfono:", null=True, blank=True)
    email = models.EmailField(verbose_name="Correo electrónico:", null=True, blank=True)#requerido
    fiscal_regimen = models.ForeignKey(FiscalRegimen, on_delete=models.PROTECT, verbose_name="Régimen fiscal:", null=True, blank=True)#requerido
    cfdi_use = models.ForeignKey(CfdiUse, on_delete=models.PROTECT, verbose_name="Uso de la factura:", null=True, blank=True)#requerido
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_customers') #empleado que hizó el registro
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio

    class Meta:
        indexes = [models.Index(fields=['name','email','uuid','rfc']),]   

    def get_full_name(self):
        customer_name = self.name
        if self.paternal_surname:
            customer_name += f" {self.paternal_surname}"
        if self.maternal_surname:
            customer_name += f" {self.maternal_surname}"
        return customer_name

    def get_direction(self):
        direction = ''
        if self.street: 
            direction += f"{self.street}" 
        if self.no_int: 
            direction += f" No. Int: {self.no_int}"             
        if self.no_ext: 
            direction += f" No. Ext: {self.no_ext}"
        return direction                     

    def __str__(self):
        return self.get_full_name()

#Caja de cobro: Ingresos,Cedula Catastral, finanzas, catastro 1, catastro 2
class CashRegister(models.Model):
    status_CHOICES = [
        ('active', 'ACTIVA'),
        ('deactivate',  'DESACTIVADA'),
    ]    
    id=models.AutoField(primary_key=True)
    key = models.CharField(verbose_name="Clave:",max_length=5, unique=True, blank=True, null=True)
    name = models.CharField(verbose_name="Nombre de caja:", max_length=50, unique=True)
    location = models.CharField(verbose_name="Ubicación", max_length=100, blank=True, null=True)
    status = models.CharField(verbose_name="Estatus de caja:",max_length=20, choices=status_CHOICES, default='deactivate')
    employee = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        row = f"Caja: {self.name} - Ubicación: {self.location}"
        return row
    
    class Meta:
        ordering = ['id']   

class CashierSession(models.Model):
    id = models.AutoField(primary_key=True)
    cash_register = models.ForeignKey(CashRegister, verbose_name="Caja:",on_delete=models.PROTECT,related_name="sessions")
    employee = models.ForeignKey(User, verbose_name="Empleado:",on_delete=models.PROTECT)     
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio        

#FEDERAL,CAJA
class IncomeType(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre:", unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        row = self.name
        return row 

class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Banco:", unique=True)

    def __str__(self):
        row = self.name
        return row 

class BankAccount(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(verbose_name="Número de cuenta:", unique=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT)
    description = models.TextField(verbose_name="Descripción:", blank=True, null=True)

    def __str__(self):
        row = f"{self.bank.name} - {self.account} - {self.description}"
        return row
    
class Category(models.Model):
    IncomeType_CHOICES = [
        ('caja', 'Caja'),
        ('federal',  'Federal'),
    ]    
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    name = models.CharField(verbose_name="Nombre de la Categoría/Ramo:", unique=True)
    income_type = models.CharField(verbose_name="Tipo de ingreso:", max_length=10, choices=IncomeType_CHOICES, default='caja')
    #income_type = models.ForeignKey(IncomeType, verbose_name="Tipo de ingreso:", related_name="income_type", on_delete=models.PROTECT) 

    class Meta:
        indexes = [models.Index(fields=['account_number','name']),]   

    def __str__(self):
        row = f"{self.account_number} - {self.name}"
        return row

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, verbose_name="Categoría/Ramo:", related_name="subcategories", on_delete=models.CASCADE)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    name = models.CharField(verbose_name="Nombre de la subcategoría:", unique=True)

    class Meta:
        indexes = [models.Index(fields=['account_number','name']),]

    def __str__(self):
        row = f"{self.account_number} - {self.name}"
        return row

class Concept(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, verbose_name="Categoría/Ramo:", related_name="category_concepts", on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, verbose_name="Subcategoría:", related_name="subcategory_concepts", on_delete=models.PROTECT)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)#IdentificationNumber
    name = models.CharField(verbose_name="Nombre del concepto:", unique=True)#Name
    description = models.TextField(verbose_name="Descripción del producto, o nombre ampliado", blank=True, null=True) #Description 
    unit_price = models.DecimalField(verbose_name="Precio unitario:", max_digits=10, decimal_places=2, default=0.00)#Price
    bank_account = models.ForeignKey(BankAccount, verbose_name="Cuenta bancaria:", on_delete=models.PROTECT, blank=True, null=True)
    predial = models.BooleanField(verbose_name="¿Es un concepto del predial?", default=False)
    online_payment = models.BooleanField(verbose_name="¿Este concepto se puede pagar en linea por el cliente?", default=False)
    #Datos de facturama
    Unit = models.CharField(verbose_name="Unidad:", max_length=20, default="Servicio", blank=True, null=True)
    UnitCode = models.ForeignKey(UnitCode, verbose_name="Código de la unidad de medida según el catálogo del SAT", on_delete=models.PROTECT, blank=True, null=True)
    CodeProdServ = models.CharField(verbose_name="Clave del Producto o servicio segun el catalogo del SAT :", max_length=20, blank=True, null=True)
    CodeProdServName = models.CharField(verbose_name="Nombre del Producto o servicio segun el catalogo del SAT:", max_length=200, blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['account_number','name']),]
        unique_together = ('category', 'subcategory','account_number')

    def __str__(self):
        row = f"{self.account_number} - {self.name}"
        return row 

class ConceptTax(models.Model): 
    id = models.AutoField(primary_key=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name="taxes" )
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE )       

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, unique=True, default=uuid.uuid4)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE) #product
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.concept.unit_price

#cash-Efectivo
#card-Tarjeta de Crédito/Débito
#transfer-Transferencia Bancaria 
#paypal-PayPal
#stripe-Stripe
#oxxo-OXXO
#spei-SPEI
#wallet-Wallet Digital
class PaymentForm(models.Model):
    id=models.AutoField(primary_key=True)
    clave = models.CharField(verbose_name="clave:", unique=True)
    name = models.CharField(verbose_name="Forma de pago:", unique=True) 
    #description = models.TextField(blank=True, null=True)
    #is_active = models.BooleanField(default=True)
    #requires_online = models.BooleanField(default=True)
    #processing_fee_percentage = models.DecimalField(
    #    max_digits=5, decimal_places=4, default=0,
    #    validators=[MinValueValidator(0), MaxValueValidator(100)]
    #)#porcentaje de tarifa de procesamiento
    #fixed_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)#Tarifa fija
    
    class Meta:
        indexes = [models.Index(fields=['clave','name']),]    

    def __str__(self):
        return self.name
#PUE-Pago en una sola exhibición
#PPD – Pago en parcialidades o diferido
class PaymentMethod(models.Model):
    id=models.AutoField(primary_key=True)
    clave = models.CharField(verbose_name="clave:", unique=True)
    name = models.CharField(verbose_name="Metodo de pago:", unique=True) 
    description = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [models.Index(fields=['clave','name']),]   

    def __str__(self):
        return self.name    
#TRANSITO
#PAGADO
#PENDIENTE
#PROCESADO
class PaymentStatus(models.Model):
    #id=models.AutoField(primary_key=True)
    name = models.CharField( verbose_name="Estatus del pago:", unique=True, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Currency(models.Model):
    #id=models.AutoField(primary_key=True)
    clave = models.CharField(verbose_name="clave:", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Nombre:", unique=True)

    def __str__(self):
        return f"{self.clave}-{self.name}"

class Invoice(models.Model):
    PaymentForm_CHOICES = [
        ('cash', 'Efectivo'),
        ('card', 'Tarjeta de Crédito/Débito'),
        ('transfer', 'Transferencia Bancaria '),
        ('spei', 'SPEI'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('oxxo', 'OXXO'),
        ('wallet', 'Wallet Digital'),
    ]      
    PaymentMethod_CHOICES = [
        ('PUE', 'Pago en una sola exhibición'),
        ('PPD', 'Pago en parcialidades o diferido'),
    ]    
    PaymentStatus_CHOICES = [
        ('pagado', 'PAGADO'),
        ('transito', 'TRANSITO'),
        ('pendiente', 'PENDIENTE'),
        
    ] 
    Currency_CHOICES = [
        ('MXN', 'Pesos'),        
    ]  
            
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    folio = models.CharField(verbose_name="Folio:", max_length=50)
    customer = models.ForeignKey(Customer, verbose_name="Cliente:", on_delete=models.PROTECT)
    payment_form = models.ForeignKey(PaymentForm, verbose_name="Forma de pago:", on_delete=models.PROTECT)
    #pay_form = models.CharField(verbose_name="Forma de pago:", max_length=30, choices=PaymentForm_CHOICES, default='cash')
    #customer_email = models.EmailField(blank=True, null=True)
    invoice = models.BooleanField(verbose_name="Requiere factura:", default=False)
    currency = models.ForeignKey(Currency, verbose_name="Moneda:", on_delete=models.PROTECT, default='MXN') #moneda
    #currency = models.CharField(verbose_name="Moneda:", max_length=10, choices=Currency_CHOICES, default='MXN')
    stripe_payment_intent_id = models.CharField(max_length=200, blank=True, null=True)
    #Montos
    subtotal = models.DecimalField(verbose_name="Subtotal:",max_digits=10, decimal_places=2, default=0.00)#importe
    tax_amount = models.DecimalField(verbose_name="Importe del impuesto:",max_digits=10, decimal_places=2, default=0.00)#impuesto
    discount_amount = models.DecimalField(verbose_name="Importe de descuento:", max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(verbose_name="Importe total:",max_digits=10, decimal_places=2) # Campo calculado
    paid_amount = models.DecimalField(verbose_name="Importe pagado",max_digits=10, decimal_places=2) # Campo calculado
    payment_method = models.ForeignKey(PaymentMethod, verbose_name="Metodo de pago:", on_delete=models.PROTECT)
    #payment_method = models.CharField(verbose_name="Metodo de pago:", max_length=10, choices=PaymentMethod_CHOICES, default='PUE')
    reference = models.CharField(verbose_name="Referencia:", max_length=100, blank=True, null=True) # Para identificar la transacción (ej. ID de PayPal)
    #Metadatos
    notes = models.TextField(verbose_name="Notas:",blank=True)
    #terms_and_conditions = models.TextField(verbose_name="Terminos y condiciones:",blank=True)    
    #payment_status = models.ForeignKey(PaymentStatus,verbose_name="Estado del pago:", on_delete=models.PROTECT)
    payment_status = models.CharField(verbose_name="Estado de pago:", max_length=10, choices=PaymentStatus_CHOICES, default='pagado')
    employee = models.ForeignKey(User,verbose_name="Empleado:", on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_payments') #pagos_registrados_por_empleado
    cash_register = models.ForeignKey(CashRegister,verbose_name="Caja:", on_delete=models.SET_NULL, null=True, blank=True, related_name='cash_registers') #pagos_registrados_por_empleado
    #fechas
    #date = models.DateField(verbose_name="Fecha",null=True, blank=True)
    issue_date = models.DateTimeField(verbose_name="Fecha de emisión:", default=timezone.now)#fecha de emision
    due_date = models.DateTimeField(verbose_name="Fecha del vencimiento:", null=True, blank=True)#fecha de vencimiento
    paid_date = models.DateTimeField(verbose_name="Fecha del pago:", null=True, blank=True)#Fecha de pago
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio

    # Campos para CFDI
    cfdi_id = models.CharField(max_length=36, blank=True, null=True, unique=True, verbose_name="Id del CFDI")
    cfdi_uuid = models.CharField(max_length=36, blank=True, null=True, unique=True, verbose_name="UUID del CFDI")
    cfdi_xml = models.FileField(upload_to='cfdi/xml/%Y/%m/', blank=True, null=True, verbose_name="XML del CFDI")
    cfdi_pdf = models.FileField(upload_to='cfdi/pdf/%Y/%m/', blank=True, null=True, verbose_name="PDF del CFDI")
    cfdi_status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Borrador'),
            ('active', 'Activo'),
            ('cancelled', 'Cancelado'),
        ],
        default='draft',
        verbose_name="Estado del CFDI"
    )
    cfdi_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de timbrado")
    cfdi_cancellation_date = models.DateTimeField(blank=True, null=True, verbose_name="Fecha de cancelación")
    
    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"
    
    def __str__(self):
        return f"{self.folio} - {self.cfdi_uuid or 'Sin timbrar'}"

    def save(self, *args, **kwargs):
        if not self.employee:
            employee = 00
        else:
            employee = self.employee.id
        if not self.folio:
            self.folio = f"{self.cash_register.key}-{employee}-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount
    
    @property
    def is_fully_paid(self):
        return self.paid_amount >= self.total_amount

    class Meta:
        indexes = [models.Index(fields=['customer']),]   
        ordering = ['-created_at']

    #def __str__(self):
    #    return f"Pago de {self.total_amount} por {self.customer.get_full_name()}"

class InvoiceItem(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.ForeignKey(Invoice, verbose_name="Factura:", related_name='items', on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, verbose_name="Concepto:", on_delete=models.CASCADE)
    description = models.CharField(verbose_name="Descripción:", null=True, blank=True)
    quantity = models.DecimalField(verbose_name="Cantidad:", max_digits=10, decimal_places=4, default=1)
    unit_price = models.DecimalField(verbose_name="Precio unitario:", max_digits=10, decimal_places=2, default=0.00)
    # Descuentos a nivel de línea
    discount_percentage = models.DecimalField(verbose_name="Porcentaje de descuento:", max_digits=5, decimal_places=2, default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(verbose_name="Importe de descuento:", max_digits=10, decimal_places=2, default=0)
    # Impuestos
    tax_rate = models.DecimalField(verbose_name="Tasa de impuesto:", max_digits=5, decimal_places=4, default=0) #tasa de impuesto
    tax_amount = models.DecimalField(verbose_name="Importe de impuesto:", max_digits=10, decimal_places=2, default=0) 
    # Totales
    #subtotal: se calcula solo
    subtotal = models.DecimalField(verbose_name="Subtotal:",max_digits=12, decimal_places=2, default=0)
    #total:se calcula solo
    total = models.DecimalField(verbose_name="Total:",max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio

    class Meta:
        indexes = [models.Index(fields=['invoice','concept']),]   

    def __str__(self):
        return f"{self.invoice.id} - {self.concept.name}"
    


class Payment(models.Model):
    """Registro de pagos realizados"""
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invoice = models.ForeignKey(Invoice,verbose_name="Factura:", related_name='payments', on_delete=models.PROTECT,null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, verbose_name="Metodo de pago:", on_delete=models.SET_NULL, null=True)
    
    amount = models.DecimalField(verbose_name="Importe:", max_digits=12, decimal_places=2)#importe
    currency = models.ForeignKey(Currency, verbose_name="Moneda:", on_delete=models.PROTECT, default='MXN') #moneda
    payment_status = models.ForeignKey(PaymentStatus,verbose_name="Estado del pago:", on_delete=models.PROTECT)
    
    # Fechas
    payment_date = models.DateTimeField(default=timezone.now)
    processed_date = models.DateTimeField(null=True, blank=True)#fecha de procesamiento
    
    # Referencias externas (gateway de pago)
    external_transaction_id = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(null=True, blank=True)#respuesta de enlace
    
    # Comisiones
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)#tarifa de procesamiento
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)#importe neto
    
    # Metadatos
    notes = models.TextField(verbose_name="Notas:",blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['invoice']),]   

    def __str__(self):
        return f"Payment {self.invoice} - {self.amount}"

class Predial(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(verbose_name="Fecha")#Fecha
    amount = models.DecimalField(verbose_name="Importe:", max_digits=12, decimal_places=2)#importe
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fecha: {self.date} - Importe:{self.amount} "

class CashPolicy(models.Model):
    id=models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    total_cash_amount = models.DecimalField(verbose_name="Importe total de caja:", max_digits=10, decimal_places=2, default=0.00)
    total_predial_amount = models.DecimalField(verbose_name="Importe total de predial:", max_digits=10, decimal_places=2, default=0.00)
    income_account = models.ForeignKey(BankAccount, verbose_name="Cuenta bancaria:", on_delete=models.PROTECT)
    amount_entered = models.DecimalField(verbose_name="Importe en la cuenta bancaria:", max_digits=10, decimal_places=2, default=0.00)
    amount_bank = models.DecimalField(verbose_name="Importe de Banco:", max_digits=10, decimal_places=2, default=0.00)
    amount_cash = models.DecimalField(verbose_name="Importe de Caja:", max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(verbose_name="Importe total:", max_digits=10, decimal_places=2, default=0.00)
    predial_portfolio = models.DecimalField(verbose_name="Importe de cartera predial:", max_digits=10, decimal_places=2, default=0.00)
    predial_backlog = models.DecimalField(verbose_name="Importe de rezago predial:", max_digits=10, decimal_places=2, default=0.00)    
    debit = models.DecimalField(verbose_name="Debe:", max_digits=10, decimal_places=2, default=0.00)
    credit = models.DecimalField(verbose_name="Haber:", max_digits=10, decimal_places=2, default=0.00)
    difference = models.DecimalField(verbose_name="Diferencia:", max_digits=10, decimal_places=2, default=0.00)
    prepare = models.CharField(verbose_name="Elaboró:",max_length=150)
    review = models.CharField(verbose_name="Revisó:",max_length=150)
    date = models.DateField(verbose_name="Fecha:",null=True, blank=True)
    issue_date = models.DateTimeField(verbose_name="Fecha de emisión:", default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio

    def __str__(self):
        #fecha = datetime.strptime(self.issue_date, '%Y-%m-%d').date()
        fecha = self.issue_date.strftime('%d/%m/%Y')
        return f"Poliza de Caja con importe: {self.total_amount} de la Fecha: {fecha}"    

class PolicyPredialItem(models.Model):
    id=models.AutoField(primary_key=True)
    policy = models.ForeignKey(CashPolicy, verbose_name="poliza", related_name='items_predial', on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, verbose_name="Concepto", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Caja:", max_digits=10, decimal_places=2, default=0.00)

class CashPolicyReceipt(models.Model):
    id=models.AutoField(primary_key=True)
    policy = models.ForeignKey(CashPolicy, verbose_name="poliza", related_name='items_receipts', on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, verbose_name="Caja", on_delete=models.CASCADE)
    start_receipt=models.CharField(verbose_name="Recibo de inicio", max_length=10)
    end_receipt=models.CharField(verbose_name="Recibo de fin", max_length=10)

class FederalPolicy(models.Model):
    id=models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    amount_bank = models.DecimalField(verbose_name="Banco:", max_digits=10, decimal_places=2, default=0.00)
    amount_cash = models.DecimalField(verbose_name="Caja:", max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(verbose_name="Importe Total:", max_digits=10, decimal_places=2, default=0.00)
    prepare = models.CharField(verbose_name="Elaboró:",max_length=150)
    review = models.CharField(verbose_name="Revisó:",max_length=150)
    date = models.DateField(verbose_name="Fecha:",null=True, blank=True)        
    issue_date = models.DateTimeField(verbose_name="Fecha de emisión:", default=timezone.now)#fecha de emision
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio

    def __str__(self):
        #fecha = datetime.strptime(self.issue_date, '%Y-%m-%d').date()
        fecha = self.issue_date.strftime('%d/%m/%Y')
        return f"Poliza Federal con importe: {self.total_amount} de la Fecha: {fecha}"      

class FederalPolicyItem(models.Model):    
    id=models.AutoField(primary_key=True)
    policy = models.ForeignKey(FederalPolicy, verbose_name="Poliza", on_delete=models.CASCADE, related_name='items_federal', null=True, blank = True)
    concept = models.ForeignKey(Concept, verbose_name="Concepto", on_delete=models.CASCADE, related_name='items_policy_federal' )
    bank_account = models.ForeignKey(BankAccount, verbose_name="Cuenta de banco", on_delete=models.CASCADE)
    amount = models.DecimalField(verbose_name="Importe:", max_digits=10, decimal_places=2, default=0.00)

class Turn(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre del giro:", max_length=200)

    def __str__(self):
        return self.name

class OperatingLicense(models.Model):
    bouquets_CHOICES = [
        ('industria', 'Industria'),
        ('comercio', 'Comercio'), 
        ('servicio', 'Servicio'), 
        ('ninguno', 'Ninguno'), 
    ]

    id = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=20, unique=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    customer = models.ForeignKey(Customer, verbose_name="Cliente", on_delete=models.PROTECT)
    trade_name = models.CharField(verbose_name="Nombre comercial del establecimiento:", max_length=200, null=True, blank=True,)
    invoice = models.ForeignKey(Invoice, verbose_name="Factura:", on_delete=models.PROTECT)
    concept = models.CharField(verbose_name="Concepto:", max_length=100, null=True, blank=True, default="AUTORIZACIÓN DEL FUNCIONAMIENTO")
    address = models.TextField(verbose_name="Dirección", null=True, blank=True)
    bouquet = models.CharField(verbose_name="Ramo:", max_length=10, choices=bouquets_CHOICES, null=True, blank=True)
    turn=models.ForeignKey(Turn, verbose_name="Giro:", on_delete=models.PROTECT, null=True, blank=True)
    employee = models.ForeignKey(User,verbose_name="Empleado:", on_delete=models.PROTECT) #pagos_registrados_por_empleado
    #date = models.DateField(verbose_name="Fecha:",null=True, blank=True)        
    issue_date = models.DateTimeField(verbose_name="Fecha de emisión:", default=timezone.now)#fecha de emision
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio    

    def save(self, *args, **kwargs):
        if not self.folio:
            self.folio = f"LF-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Licencia de funcionamiento: {self.folio} - {self.customer.name}"
    
class Quotation(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    folio = models.CharField(verbose_name="Folio:", max_length=100, unique=True)
    dependence = models.ForeignKey(dependence, verbose_name="Dependencia:", on_delete=models.PROTECT)
    department = models.ForeignKey(department, verbose_name="Departamento:", on_delete=models.PROTECT)
    subject = models.CharField(verbose_name="Asunto:", max_length=100)
    customer = models.ForeignKey(Customer, verbose_name="Dependencia:", on_delete=models.PROTECT)
    introduction = models.TextField(verbose_name="Introduction:")
    total_amount = models.DecimalField(verbose_name="Total:",max_digits=12, decimal_places=2, default=0)
    conclusion = models.TextField(verbose_name="Conclusión:")
    employee = models.ForeignKey(User, verbose_name="Empleado:", on_delete=models.PROTECT, null=True, blank=True)
    issue_date = models.DateTimeField(verbose_name="Fecha de emisión:", default=timezone.now)#fecha de emision
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio  

    def save(self, *args, **kwargs):
        if not self.folio:
            self.folio = f"TM/IN/{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago de {self.total_amount} por {self.customer.get_full_name}"        

class QuotationItem(models.Model):
    id = models.AutoField(primary_key=True)
    quotation = models.ForeignKey(Quotation, verbose_name="Cotización:", related_name='items', on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, verbose_name="Concepto:", on_delete=models.CASCADE)
    description = models.CharField(verbose_name="Descripción:", null=True, blank=True)
    quantity = models.DecimalField(verbose_name="Cantidad:", max_digits=10, decimal_places=4, default=1)
    unit_price = models.DecimalField(verbose_name="Precio unitario:", max_digits=10, decimal_places=2, default=0.00)
    # Descuentos a nivel de línea
    discount_percentage = models.DecimalField(verbose_name="Porcentaje de descuento:", max_digits=5, decimal_places=2, default=0,validators=[MinValueValidator(0), MaxValueValidator(100)])
    discount_amount = models.DecimalField(verbose_name="Importe de descuento:", max_digits=10, decimal_places=2, default=0)
    # Impuestos
    tax_rate = models.DecimalField(verbose_name="Tasa de impuesto:", max_digits=5, decimal_places=4, default=0) #tasa de impuesto
    tax_amount = models.DecimalField(verbose_name="Importe de impuesto:", max_digits=10, decimal_places=2, default=0) 
    # Totales
    #subtotal: se calcula solo
    subtotal = models.DecimalField(verbose_name="Subtotal:",max_digits=12, decimal_places=2, default=0)
    #total:se calcula solo
    total = models.DecimalField(verbose_name="Total:",max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio        

    class Meta:
        indexes = [models.Index(fields=['quotation','concept']),]   

    def __str__(self):
        return f"{self.quotation.id} - {self.concept.name}"
    
    def save(self, *args, **kwargs):
        # Calcular totales automáticamente
        self.subtotal = self.quantity * self.unit_price
        if self.discount_percentage > 0:
            self.discount_amount = self.subtotal * (self.discount_percentage / 100)
        
        subtotal_after_discount = self.subtotal - self.discount_amount
        self.tax_amount = subtotal_after_discount * (self.tax_rate / 100)
        self.total = subtotal_after_discount + self.tax_amount
        
        super().save(*args, **kwargs)    