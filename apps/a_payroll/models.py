from django.db import models

# Create your models here.
class Dependence(models.Model):
    key = models.CharField(verbose_name="Ramo:", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Dirección:", unique=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"  
    
class Category(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Dirección:", unique=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"  

class Type(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Tipo:", unique=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"      
    
class Movement(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Movimiento:", unique=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"       
    
class TypeEmployee(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Tipo de empleado:", unique=True) #PENSIONADOS,BASE,SINDICALIZADO....
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"       
    
class TypePayroll(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Tipo de nomina:", unique=True) #B,P,E....
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"

class Bank(models.Model):
    name = models.CharField(verbose_name="Banco:", unique=True)

    def __str__(self):
        row = self.name
        return row 

class WorkingDay(models.Model):
    name = models.CharField(verbose_name="Jornada:", unique=True)

    def __str__(self):
        row = self.name
        return row     
class TypeSalary(models.Model):
    name = models.CharField(verbose_name="Tipo de salario:", unique=True)

    def __str__(self):
        row = self.name
        return row     
    
class TaxRegime(models.Model):
    name = models.CharField(verbose_name="Regimen fiscal:", unique=True)

    def __str__(self):
        row = self.name
        return row   

class Employee(models.Model): 
    sex = [
        ("F", "F"),
        ("M", "M"),
    ]
    key = models.CharField(verbose_name="cve_empleado", unique=True, primary_key=True)
    paternal_surname = models.CharField(verbose_name="Apellido paterno:", max_length=50, null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Apellido materno:", max_length=50, null=True, blank=True)            
    name = models.CharField(verbose_name="Nombre:", max_length=100, null=True, blank=True)
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    base_date = models.DateTimeField(blank=True, null=True)
    contract_date = models.DateTimeField(blank=True, null=True)
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    birth_date = models.DateTimeField(blank=True, null=True)
    sex = models.CharField(verbose_name="Sexo:",choices=sex, null=True, blank=True)
    account_no = models.BigIntegerField(verbose_name="Número de cuenta:", null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT)
    working_day = models.ForeignKey(WorkingDay, verbose_name="Jornada:", on_delete=models.PROTECT)
    type_salary = models.ForeignKey(TypeSalary, verbose_name="Tipo de salario:", on_delete=models.PROTECT)
    tax_regime = models.ForeignKey(TaxRegime, verbose_name="Régimen fiscal:", on_delete=models.PROTECT)
    dependence = models.ForeignKey(Dependence, verbose_name="Departamento:", on_delete=models.PROTECT)
    category = models.ForeignKey(Category, verbose_name="Puesto:", on_delete=models.PROTECT)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT)