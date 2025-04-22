from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    person_type = [(1, "Persona física"), (2, "Persona moral")]
    person_type = models.IntegerField(verbose_name="Tipo de contributente:", choices=person_type)
    rfc = models.CharField(verbose_name="RFC", max_length=13, unique=True, null=True, blank=True)
    name = models.CharField(verbose_name="Nombre:", max_length=100)
    paternalsurname = models.CharField(verbose_name="Primer apellido:", max_length=50, null=True, blank=True)
    maternalsurname = models.CharField(verbose_name="Segundo apellido:", max_length=50, null=True, blank=True)
    country = models.CharField(verbose_name="Pais:", null=True, blank=True)
    state = models.CharField(verbose_name="Estado:", null=True, blank=True)
    municipality = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    colony = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    postal_code = models.CharField(verbose_name="Código portal:", null=True, blank=True)
    street = models.CharField(verbose_name="Calle:", max_length=200)
    no_ext = models.CharField(verbose_name="No.Ext:", max_length=10, null=True, blank=True)
    no_int = models.CharField(verbose_name="No.Int:", max_length=10, null=True, blank=True)
    reference = models.CharField(verbose_name="Referencia:", null=True, blank=True)
    cellphone = models.CharField(verbose_name="Celular:", unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="Correo electrónico:", unique=True, null=True, blank=True)

    def __str__(self):
        row = f"{self.name} {self.paternalsurname} {self.maternalsurname}"
        return row 
#FEDERAL,CAJA
class IncomeType(models.Model):
    name = models.CharField(verbose_name="Nombre:", unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        row = self.name
        return row 


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    name = models.CharField(verbose_name="Nombre de la Categoría/Ramo:", unique=True)
    income_type = models.ForeignKey(IncomeType, verbose_name="Tipo de ingreso:", related_name="income_type", on_delete=models.PROTECT) 

    def __str__(self):
        row = self.name
        return row

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, verbose_name="Categoría/Ramo:", related_name="my_category", on_delete=models.CASCADE)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    name = models.CharField(verbose_name="Nombre de la subcategoría:", unique=True)

    def __str__(self):
        row = self.name
        return row

class Bank(models.Model):
    #id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Banco:", unique=True)

    def __str__(self):
        row = self.name
        return row 


class BankAccount(models.Model):
    account = models.BigIntegerField(verbose_name="Número de cuenta:", unique=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT)

    def __str__(self):
        row = f"{self.bank.name} - {self.account}"
        return row


class Concept(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    category = models.ForeignKey(Category, verbose_name="Categoría/Ramo:", related_name="category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, verbose_name="Subcategoría:", related_name="subcategory", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('category', 'subcategory')
    name = models.CharField(verbose_name="Nombre del concepto:", unique=True)
    bank_account = models.ForeignKey(BankAccount, verbose_name="Cuenta bancaria:", on_delete=models.PROTECT)

    def __str__(self):
        row = f"{self.account_number} - {self.name}"
        return row 
    
#TARJETA, TRANSFERENCIA BANCARIA, EFECTIVO, BILLETERA ELECTRONICA 
class PaymentForm(models.Model):
    name = models.CharField(verbose_name="Forma de pago:", unique=True) 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
#TARJETA: Visa, MasterCard, American Express
# TRANSFERENCIA: SPEI (México) 
#EFECTIVO: MONEDA LOCA
#BILLETERA ELECTRONICA: PayPal, Mercado Pago
class PaymentMethod(models.Model):
    payment_form = models.ForeignKey(PaymentForm, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Metodo de pago:", unique=True) 
    class Meta:
        unique_together = ('payment_form', 'name') 
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.payment_form.name} - {self.name}"    

class PaymentStatus(models.Model):
    name = models.CharField(verbose_name="Estatus del pago:", unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Pay(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, verbose_name="Cliente:", on_delete=models.CASCADE)
    pay_form = models.ForeignKey(PaymentForm, on_delete=models.PROTECT)
    invoice = models.BooleanField(verbose_name="Requiere factura:", default=False)
    concept = models.ForeignKey(Concept, verbose_name="Concepto:", related_name="concept_in_payments", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2) # Campo calculado
    payment_method = models.ForeignKey(PaymentMethod, verbose_name="Metodo de pago:", on_delete=models.PROTECT)
    account_number = models.CharField(max_length=100, blank=True, null=True) # Puede ser opcional
    reference = models.CharField(max_length=255, blank=True, null=True) # Para identificar la transacción (ej. ID de PayPal)
    payment_status = models.ForeignKey(PaymentStatus, on_delete=models.PROTECT)
    additional_details = models.JSONField(blank=True, null=True)
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='recorded_payments') #pagos_registrados_por_empleado
    approval_date = models.DateTimeField(blank=True, null=True) #Fecha de aprobación del pago
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio


class DetailPay(models.Model):
    id = models.AutoField(primary_key=True)
    concept = models.ForeignKey(Concept, verbose_name="Concepto", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Cantidad:", default=1)
    description = models.CharField(verbose_name="Descripción:", null=True, blank=True)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)



