from django.db import models


# Create your models here.
class Customer(models.Model):
    person_type = [(1, "Persona física"), (2, "Persona moral")]
    id = models.AutoField(primary_key=True)
    person_type = models.IntegerField(
        verbose_name="Tipo de contributente:", choices=person_type
    )
    rfc = models.CharField(
        verbose_name="RFC", max_length=13, unique=True, null=True, blank=True
    )
    name = models.CharField(verbose_name="Nombre:", max_length=100)
    paternalsurname = models.CharField(
        verbose_name="Primer apellido:", max_length=50, null=True, blank=True
    )
    maternalsurname = models.CharField(
        verbose_name="Segundo apellido:", max_length=50, null=True, blank=True
    )
    country = models.CharField(verbose_name="Pais:", null=True, blank=True)
    state = models.CharField(verbose_name="Estado:", null=True, blank=True)
    municipality = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    colony = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    postal_code = models.CharField(verbose_name="Código portal:", null=True, blank=True)
    # locality = models.CharField(verbose_name="Localidad:", null=True, blank=True)
    street = models.CharField(verbose_name="Calle:", max_length=200)
    no_ext = models.CharField(
        verbose_name="No.Ext:", max_length=10, null=True, blank=True
    )
    no_int = models.CharField(
        verbose_name="No.Int:", max_length=10, null=True, blank=True
    )
    reference = models.CharField(verbose_name="Referencia:", null=True, blank=True)
    cellphone = models.CharField(
        verbose_name="Celular:", unique=True, null=True, blank=True
    )
    email = models.EmailField(
        verbose_name="Correo electrónico:", unique=True, null=True, blank=True
    )

    def __str__(self):
        row = f"{self.name} {self.paternalsurname} {self.maternalsurname}"
        return row


class IncomeType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Nombre:", unique=True)

    def __str__(self):
        row = self.name
        return row


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    name = models.CharField(verbose_name="Nombre de la Categoría/Ramo:", unique=True)
    income_type = models.ForeignKey(
        IncomeType, verbose_name="Tipo de ingreso:", on_delete=models.CASCADE
    )

    def __str__(self):
        row = self.name
        return row


class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    category = models.ForeignKey(
        Category, verbose_name="Categoría/Ramo:", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="Nombre de la subcategoría:", unique=True)

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
    account = models.BigIntegerField(verbose_name="Número de cuenta:", unique=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.CASCADE)

    def __str__(self):
        row = f"{self.bank.name} - {self.account}"
        return row


class Concept(models.Model):
    id = models.AutoField(primary_key=True)
    account_number = models.CharField(verbose_name="Cuenta contable:", unique=True)
    category = models.ForeignKey(
        Category, verbose_name="Categoría/Ramo:", on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        Subcategory, verbose_name="Subcategoría:", on_delete=models.CASCADE
    )

    name = models.CharField(verbose_name="Nombre del concepto:", unique=True)
    bank_account = models.ForeignKey(
        BankAccount, verbose_name="Cuenta bancaria:", on_delete=models.CASCADE
    )

    def __str__(self):
        row = self.name
        return row


class MethodPayment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Metodo de pago:", unique=True)


class Pay(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, verbose_name="Cliente:", on_delete=models.CASCADE
    )
    method_payment = models.ForeignKey(
        MethodPayment, verbose_name="Metodo de pago:", on_delete=models.CASCADE
    )
    no_cuenta = models.BigIntegerField(
        verbose_name="Número de cuenta / Referencia bancaria:", null=True, blank=True
    )
    invoice = models.BooleanField(verbose_name="Factura:")
    created_at = models.DateTimeField(auto_now_add=True)  # Se fija al crear el objeto
    updated_at = models.DateTimeField(auto_now=True)  # Se actualiza en cada cambio


class DetailPay(models.Model):
    id = models.AutoField(primary_key=True)
    concept = models.ForeignKey(
        Concept, verbose_name="Concepto", on_delete=models.CASCADE
    )
    quantity = models.IntegerField(verbose_name="Cantidad:", default=1)
    description = models.CharField(verbose_name="Descripción:", null=True, blank=True)
    unit_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
