from django.db import models

# Create your models here.
# TODO: CATÁLOGOS
class Dependence(models.Model):
    key = models.CharField(verbose_name="Ramo:", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Dirección:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.name}"  
    
class Position(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Puesto:", unique=True) 
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.name}"  

class Type(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Tipo:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True)  
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"      
    
class Movement(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Movimiento:", unique=True) 
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"       
    
class TypeEmployee(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True) #N, S,NS
    name = models.CharField(verbose_name="Tipo de empleado:", unique=True) #PENSIONADOS,BASE,SINDICALIZADO....
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"       
    
class TypePayroll(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True) #B,P,E
    name = models.CharField(verbose_name="Tipo de nomina:", unique=True) #B,P,E....
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"

class Bank(models.Model):
    name = models.CharField(verbose_name="Banco:", unique=True, primary_key=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row 

class WorkDay(models.Model):
    name = models.CharField(verbose_name="Jornada:", unique=True, primary_key=True)#DIRUNA, JUBILADO
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TypeSalary(models.Model):
    name = models.CharField(verbose_name="Tipo de salario:", unique=True, primary_key=True) #MIXTO, UNICO
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TaxRegime(models.Model): #JUBILADOS, SUELDOS Y SALARIOS
    name = models.CharField(verbose_name="Regimen fiscal:", unique=True, primary_key=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row   
    
#TODO-CATEGORIAS
class Category(models.Model):
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        #unique_together = ('position', 'type_employee','type_payroll')
        indexes = [models.Index(fields=['position', 'type_employee','type_payroll'])]
        constraints = [
            models.UniqueConstraint(
                fields=['position', 'type_employee', 'type_payroll'],
                name='unique_category'
            )
        ]
    def __str__(self):
        return f"{self.position} ( {self.type_employee} | {self.type_payroll} )"

#TODO-CONCEPTOS-(PERCEPCIONES Y DEDUCCIONES)
class Concept(models.Model):
    PERCEPTION = 'P'
    DEDUCTION  = 'D'
    TYPE_CHOICES = [
        (PERCEPTION, 'Percepción'),
        (DEDUCTION,  'Deducción'),
    ]
    name        = models.CharField("Nombre del atributo", unique=True, max_length=100)
    type        = models.CharField("Tipo", max_length=1, choices=TYPE_CHOICES)
    description = models.TextField("Descripción", blank=True, null=True)

    def __str__(self):
        #return f"{self.get_type_display()}: {self.name}"
        return self.name

#TODO-TABULADOR DE SUELDOS
class CategoryConcept(models.Model):
    category  = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='concepts')
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT, related_name='values')
    value     = models.DecimalField("Valor", max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('category', 'concept')
        ordering = ('concept__type', 'concept__name')
        indexes = [models.Index(fields=['category'])]

    def __str__(self):
        return f"{self.category} • {self.concept}: {self.value}"
    
# TODO: EMPLEADOS
class Empleado(models.Model):
    #cve_emp
    key = models.CharField(verbose_name="cve_empleado", unique=True, primary_key=True)
    #apellido-p
    ape_paterno = models.CharField(verbose_name="Apellido paterno:", null=True, blank=True)
    #apellido-m
    ape_materno = models.CharField(verbose_name="Apellido materno:", null=True, blank=True)
    #nombre            
    nombre = models.CharField(verbose_name="Nombre:", null=True, blank=True)
    #rfc
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    #curp
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    #fecha de base
    fecha_base =  models.CharField(verbose_name="Fecha de base:", null=True, blank=True)
    #fecha de contrato
    fecha_contrato =  models.CharField(verbose_name="Fecha de contrato:", null=True, blank=True)
    #nss
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    #codigo postal
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    #fecha de nacimiento
    fecha_nacimiento =  models.CharField(verbose_name="Fecha de nacimiento:", null=True, blank=True)
    #sexo
    sexo = models.CharField(verbose_name="Sexo:", null=True, blank=True)
    #num de cuenta
    num_cuenta =  models.CharField(verbose_name="Número de cuenta:", null=True, blank=True)
    #banco
    banco =  models.CharField(verbose_name="Banco:", null=True, blank=True)
    #jornada    
    jornada =  models.CharField(verbose_name="Jornada:", null=True, blank=True)
    #tipo salario
    tipo_salario =  models.CharField(verbose_name="Tipo de salario:", null=True, blank=True)
    #regimen 
    regimen =  models.CharField(verbose_name="Régimen fiscal:", null=True, blank=True)
    #QNA-quincena
    qna = models.CharField(verbose_name="QNA:", null=True, blank=True)
    #periodo fecha1 - fecha2
    periodo = models.CharField(verbose_name="Periodo:", null=True, blank=True)
    #departamento
    departamento = models.CharField(verbose_name="Departamento:", null=True, blank=True)
    #puesto
    puesto = models.CharField(verbose_name="Puesto:", null=True, blank=True)
    #dias pagados
    dias_pagados = models.CharField(verbose_name="Dias pagados:", null=True, blank=True)
    #ramo_id
    ramo_id = models.CharField(verbose_name="Ramo:", null=True, blank=True)
    #cve_pto_id
    cve_pto_id = models.CharField(verbose_name="cve_pto:", null=True, blank=True)
    #tipo de empleado
    tipo_empleado_id = models.CharField(verbose_name="sindicato:", null=True, blank=True)
    #tipo de nomina
    tipo_nomina_id = models.CharField(verbose_name="nomina:", null=True, blank=True)
    #tipo
    tipo = models.CharField(verbose_name="Tipo", null=True, blank=True)
    #sueldo
    sueldo = models.CharField(verbose_name="Sueldo:",null=True, blank=True) 
    #percepciones
    percepcion = models.CharField(verbose_name="Percepciones:",null=True, blank=True)
    #deducciones
    deduccion = models.CharField(verbose_name="Deducciones:",null=True, blank=True)
    #total neto
    total_neto = models.CharField(verbose_name="Total neto:",null=True, blank=True)
    #fecha de alta    
    fecha_alta =models.CharField(verbose_name="Fecha de alta:", null=True, blank=True)
    #cve cambio id
    cve_camb_id = models.CharField(verbose_name="cve Cambio", null=True, blank=True)
    #cambio
    cambio = models.CharField(verbose_name="Cambio", null=True, blank=True)
    #edad (se calcula)
    edad = models.CharField(verbose_name="Edad", null=True, blank=True)
    #antigüedad (base y fecha actual)
    antiguedad = models.CharField(verbose_name="Antiguedad laboral", null=True, blank=True)
    #comision
    comision = models.CharField(verbose_name="Comision:", null=True, blank=True)
    #ubicacion
    ubicacion = models.CharField(verbose_name="Ubicación:", null=True, blank=True)
    #funcion
    funcion = models.CharField(verbose_name="Función:", null=True, blank=True)
    #direccion
    direccion = models.CharField(verbose_name="Dirección", null=True, blank=True) 
    #colonia
    colonia = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    #localidad
    localidad = models.CharField(verbose_name="Localidad:", null=True, blank=True)
    #municipio
    municipio = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    #estado
    estado = models.CharField(verbose_name="Estado:", null=True, blank=True)
    #lugar de nacimiento
    lugar_nacimiento = models.CharField(verbose_name="Lugar de nacimiento:", null=True, blank=True)
    #email
    email = models.CharField(verbose_name="Correo electrónico:",  null=True, blank=True)
    #telefono
    telefono = models.CharField(verbose_name="Teléfono:", null=True, blank=True)
    #fecha de baja
    fecha_baja = models.CharField(verbose_name="Fecha de baja:",blank=True, null=True)
    #nota
    nota = models.CharField(verbose_name="Nota:", null=True, blank=True) 
    class Meta:
        indexes = [models.Index(fields=['key']),]

    def __str__(self):
        return f"{self.ape_paterno} {self.ape_materno} {self.nombre}"

class Employee(models.Model):
    key = models.CharField(verbose_name="Clave de empleado:", unique=True, primary_key=True)
    paternal_surname = models.CharField(verbose_name="Apellido paterno:", max_length=50, null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Apellido materno:", max_length=50, null=True, blank=True)            
    name = models.CharField(verbose_name="Nombre:", max_length=100, null=True, blank=True)       
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    base_date = models.DateField(verbose_name="Fecha de base:",blank=True, null=True)
    contract_date = models.DateField(verbose_name="Fecha de contrato:",blank=True, null=True)
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Fecha de nacimiento:",blank=True, null=True)
    sex = [("F", "FEMENINO"),("M", "MASCULINO"),]  
    sex = models.CharField(verbose_name="Sexo:",choices=sex, null=True, blank=True)             
    account_no = models.CharField(verbose_name="Número de cuenta:", null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT, null=True, blank=True)    
    workday = models.ForeignKey(WorkDay, verbose_name="Jornada:", on_delete=models.PROTECT, null=True, blank=True)
    type_salary = models.ForeignKey(TypeSalary, verbose_name="Tipo de salario:", on_delete=models.PROTECT, null=True, blank=True)     
    tax_regime = models.ForeignKey(TaxRegime, verbose_name="Régimen fiscal:", on_delete=models.PROTECT, null=True, blank=True)
    #QNA-quincena
        #fortnight = models.CharField(verbose_name="Quincena:", null=True, blank=True)    
    #Periodo
        #period = models.CharField(verbose_name="Periodo:", null=True, blank=True)
    dependence = models.ForeignKey(Dependence, verbose_name="Departamento:", on_delete=models.PROTECT)
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT)
    type = models.ForeignKey(Type, verbose_name="Tipo", on_delete=models.PROTECT, null=True, blank=True)
    #sueldo
    #percepciones
    #deducciones
    #total_neto
    #fecha de alta
    entry_date = models.DateField(verbose_name="Fecha de alta:", null=True, blank=True)
    #cambio
    change = models.ForeignKey(Movement, verbose_name="Cambio", on_delete=models.PROTECT, null=True, blank=True)
    #edad = models.CharField(verbose_name="Edad", null=True, blank=True)
    #age = models.CharField(verbose_name="Edad", null=True, blank=True)
    #antiguedad (base y fecha actual)
    #seniority = models.CharField(verbose_name="Antiguedad laboral", null=True, blank=True)
    #comision
    commission = models.CharField(verbose_name="Comision:", null=True, blank=True)
    #ubicacion
    location = models.CharField(verbose_name="Ubicación:", null=True, blank=True)
    #funcion
    function= models.CharField(verbose_name="Función:", null=True, blank=True)
    #direccion
    address = models.CharField(verbose_name="Dirección", null=True, blank=True) 
    #coloniia
    colony = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    #localidad
    locality = models.CharField(verbose_name="Localidad:", null=True, blank=True)
    #municipio
    municipality = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    #estado
    state = models.CharField(verbose_name="Estado:", null=True, blank=True)
    #lugar de nacimiento
    place_birth = models.CharField(verbose_name="Lugar de nacimiento:", null=True, blank=True)
    #email
    email = models.CharField(verbose_name="Correo electrónico:",  null=True, blank=True)
    #telefono
    phone = models.CharField(verbose_name="Teléfono:", null=True, blank=True)
    #fecha de baja
    leaving_date = models.DateField(verbose_name="Fecha de baja:", null=True, blank=True)
    #nota
    description = models.CharField(verbose_name="Nota:", null=True, blank=True)
    employee_status = [(True,"ACTIVO"),(False,"INACTIVO")]
    status = models.BooleanField(verbose_name="Estatus del empleado:",choices=employee_status, null=True, blank=True, default=True)  

    class Meta:
        indexes = [models.Index(fields=['key']),]    
    
    def __str__(self):
        return f"{self.paternal_surname} {self.maternal_surname} {self.name}" 

class EmployeeCategory(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name='my_category')
    category = models.OneToOneField(Category, on_delete=models.CASCADE) 

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'category'],
                name='unique_employee_category'
            )
        ]

    def __str__(self):
        return self.category

class EmployeeConcept(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='concepts')
    concept = models.ForeignKey(Concept, on_delete=models.PROTECT)
    value     = models.DecimalField("Valor", max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee} • {self.concept}: {self.value}"        

# TODO: PRENÓMINA
#Periodo de facturación
class Period(models.Model):
    start_date = models.DateField(verbose_name="Fecha de inicio del periodo:")
    end_date = models.DateField(verbose_name="Fecha de fin del periodo:")
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        ordering = ['start_date']
        unique_together = ('start_date', 'end_date') 
    def __str__(self):
        return f"{self.start_date} - {self.end_date} : {self.description}"


