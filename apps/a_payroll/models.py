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
    name = models.CharField(verbose_name="Banco:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row 

class WorkingDay(models.Model):
    name = models.CharField(verbose_name="Jornada:", unique=True)#DIRUNA, JUBILADO
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TypeSalary(models.Model):
    name = models.CharField(verbose_name="Tipo de salario:", unique=True) #MIXTO, UNICO
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TaxRegime(models.Model): #JUBILADOS, SUELDOS Y SALARIOS
    name = models.CharField(verbose_name="Regimen fiscal:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row   
    
#? NUEVA TABLA - ENGLOBA (PERCEPCIONES Y DEDUCCIONES)
class AttributeCatalog(models.Model):
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
        return f"{self.get_type_display()}: {self.name}"

#tabulador de sueldos quincenal
class CategoryTab(models.Model):
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        unique_together = ('position', 'type_employee','type_payroll')
        indexes = [models.Index(fields=['position', 'type_employee','type_payroll'])]

    def __str__(self):
        return f"{self.position}  - {self.type_employee} - {self.type_payroll}"
    
class CategoryAttribute(models.Model):
    category  = models.ForeignKey(CategoryTab, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(AttributeCatalog, on_delete=models.PROTECT, related_name='values')
    value     = models.DecimalField("Valor", max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('category', 'attribute')
        ordering = ('attribute__type', 'attribute__name')
        indexes = [models.Index(fields=['category'])]

    def __str__(self):
        return f"{self.category} • {self.attribute}: {self.value}"

# TODO: EMPLEADOS
class Empleado(models.Model):
    key = models.CharField(verbose_name="cve_empleado", unique=True, primary_key=True)
    paternal_surname = models.CharField(verbose_name="Apellido paterno:", null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Apellido materno:", null=True, blank=True)            
    name = models.CharField(verbose_name="Nombre:", null=True, blank=True)
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    base_date =  models.CharField(verbose_name="Fecha de base:", null=True, blank=True)
    contract_date =  models.CharField(verbose_name="Fecha de contrato:", null=True, blank=True)
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    birth_date =  models.CharField(verbose_name="Fecha de nacimiento:", null=True, blank=True)
    sex = models.CharField(verbose_name="Sexo:", null=True, blank=True)
    account_no =  models.CharField(verbose_name="Número de cuenta:", null=True, blank=True)
    bank =  models.CharField(verbose_name="Banco:", null=True, blank=True)    
    working_day =  models.CharField(verbose_name="Jornada:", null=True, blank=True)
    type_salary =  models.CharField(verbose_name="Tipo de salario:", null=True, blank=True) 
    tax_regime =  models.CharField(verbose_name="Régimen fiscal:", null=True, blank=True)
    #quincena
    qna = models.CharField(verbose_name="QNA:", null=True, blank=True)
    #periodo
    period = models.CharField(verbose_name="Periodo:", null=True, blank=True)
    text_dependence = models.CharField(verbose_name="Departamento:", null=True, blank=True)
    text_period = models.CharField(verbose_name="Puesto:", null=True, blank=True)
    text_period = models.CharField(verbose_name="Dias pagados:", null=True, blank=True)
    #dias pagados
    dependence = models.CharField(verbose_name="Ramo:", null=True, blank=True)
    position = models.CharField(verbose_name="cve_pto:", null=True, blank=True)
    type_employee = models.CharField(verbose_name="sindicato:", null=True, blank=True)
    type_payroll = models.CharField(verbose_name="nomina:", null=True, blank=True)
    type = models.CharField(verbose_name="Tipo", null=True, blank=True)

    total_salary = models.CharField(verbose_name="Total neto:",null=True, blank=True)    
    entry_date =models.CharField(verbose_name="Fecha de alta:", null=True, blank=True)
    movement = models.CharField(verbose_name="cve Cambio", null=True, blank=True)
    change = models.CharField(verbose_name="Cambio", null=True, blank=True)
    #edad (se calcula)
    age = models.CharField(verbose_name="Edad", null=True, blank=True)
    #antiguedad (base y fecha actual)
    seniority = models.CharField(verbose_name="Antiguedad laboral", null=True, blank=True)
    #COMISION
    commission = models.CharField(verbose_name="Comision:", null=True, blank=True)
    #UBICACION
    location = models.CharField(verbose_name="Ubicación:", null=True, blank=True)
    #FUNCION
    responsibility = models.CharField(verbose_name="Función:", null=True, blank=True)
    #DIRECCIÓN
    address = models.CharField(verbose_name="Dirección", null=True, blank=True) 
    #COLONIA
    colony = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    #LOCALIDAD
    locality = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    #ESTADO
    state = models.CharField(verbose_name="Estado:", null=True, blank=True)
    #LUGAR DE NACIMIENTO
    place_birth = models.CharField(verbose_name="Lugar de nacimiento:", null=True, blank=True)
    #EMAIL
    email = models.CharField(verbose_name="Correo electrónico:",  null=True, blank=True)
    #TELEFONO
    phone = models.CharField(verbose_name="Teléfono:", null=True, blank=True)
    #FECHA DE BAJA
    leaving_date = models.CharField(verbose_name="Fecha de baja:",blank=True, null=True)
    #NOTA
    description = models.CharField(verbose_name="Nota:", null=True, blank=True) 
    class Meta:
        indexes = [models.Index(fields=['key']),]

    def __str__(self):
        return f"{self.paternal_surname} {self.maternal_surname} {self.name}"

class Employee(models.Model):
    key = models.CharField(verbose_name="Clave de empleado:", unique=True, primary_key=True)
    paternal_surname = models.CharField(verbose_name="Apellido paterno:", max_length=50, null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Apellido materno:", max_length=50, null=True, blank=True)            
    name = models.CharField(verbose_name="Nombre:", max_length=100, null=True, blank=True)
    employee_status = [(True,"ACTIVO"),(False,"INACTIVO")]
    status = models.BooleanField(verbose_name="Estatus del empleado:",choices=employee_status, null=True, blank=True, default=True)

class EmployeePersonalData(models.Model): 
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name='personal_information')
    cellphone = models.CharField(verbose_name="Celular:", max_length=20, null=True, blank=True)
    phone = models.CharField(verbose_name="Teléfono:", max_length=20, null=True, blank=True)
    email = models.CharField(verbose_name="Correo electrónico:", max_length=100, null=True, blank=True)
    country = models.CharField(verbose_name="Pais:", null=True, blank=True)
    state = models.CharField(verbose_name="Estado:", null=True, blank=True)
    municipality = models.CharField(verbose_name="Municipio:", null=True, blank=True)
    postal_code = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    colony = models.CharField(verbose_name="Colonia:", null=True, blank=True)
    street = models.CharField(verbose_name="Calle:", max_length=200, null=True, blank=True)
    no_ext = models.CharField(verbose_name="No.Ext:", max_length=10, null=True, blank=True)
    no_int = models.CharField(verbose_name="No.Int:", max_length=10, null=True, blank=True)
    reference = models.CharField(verbose_name="Referencia:", null=True, blank=True)
    languages = models.TextField(verbose_name="Idiomas:", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Fecha de nacimiento:",blank=True, null=True)
    sex = [("F", "FEMENINO"),("M", "MASCULINO"),]  
    civil_statuses  = [("SOLTERO","SOLTERO"),("CASADO","CASADO"),("DIVORCIADO","DIVORCIADO"),("VIUDO","VIUDO")]
    
    sex = models.CharField(verbose_name="Sexo:",choices=sex, null=True, blank=True)    
    marital_status = models.CharField(verbose_name="Estado civil:",choices=civil_statuses, null=True, blank=True)
    

    class Meta:
        indexes = [models.Index(fields=['key']),]

    def __str__(self):
        return f"{self.paternal_surname} {self.maternal_surname} {self.name}"
    
#datos fiscales
class EmployeeTaxtData(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name='tax_information')
    tax_regime = models.ForeignKey(TaxRegime, verbose_name="Régimen fiscal:", on_delete=models.PROTECT, null=True, blank=True)    
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)

#datos laborales
class EmployeeJobData(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE,related_name='job_information')
    dependence = models.ForeignKey(Dependence, verbose_name="Departamento:", on_delete=models.PROTECT)
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT)
    #nuevo
    type = models.ForeignKey(Type, verbose_name="Tipo", on_delete=models.PROTECT, null=True, blank=True)
    total_salary = models.DecimalField(verbose_name="Salario total:", max_digits=12, decimal_places=2, default=0.00)
    #nuevo
    entry_date = models.DateField(verbose_name="Fecha de alta:", null=True, blank=True)
    #nuevo
    movement = models.ForeignKey(Movement, verbose_name="Cambio", on_delete=models.PROTECT, null=True, blank=True)
    category  = models.ForeignKey(CategoryTab, on_delete=models.CASCADE, related_name='income_category') 
    base_date = models.DateField(verbose_name="Fecha de base:",blank=True, null=True)
    contract_date = models.DateField(verbose_name="Fecha de contrato:",blank=True, null=True)
    contract_termination_date = models.DateField(verbose_name="Fecha de termino de contrato:",blank=True, null=True)
    account_no = models.BigIntegerField(verbose_name="Número de cuenta:", null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT, null=True, blank=True)
    check_in_time = models.TimeField(verbose_name="Hora de entrada", null=True, blank=True)
    check_out_time = models.TimeField(verbose_name="Hora de salida:", null=True, blank=True)
    working_day = models.ForeignKey(WorkingDay, verbose_name="Jornada:", on_delete=models.PROTECT, null=True, blank=True)
    type_salary = models.ForeignKey(TypeSalary, verbose_name="Tipo de salario:", on_delete=models.PROTECT, null=True, blank=True) 
    description = models.TextField(verbose_name="Descripción del puesto:", null=True, blank=True) 

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

class EmployeeAdjustment(models.Model):
    employee  = models.ForeignKey(Employee, on_delete=models.CASCADE,related_name='adjustments')
    #period = models.ForeignKey(Period, on_delete=models.CASCADE) 
    attribute = models.ForeignKey(AttributeCatalog, on_delete=models.PROTECT)
    value     = models.DecimalField("Valor", max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.employee} • {self.attribute}: {self.value}"

# TODO: PRENÓMINA

#Prenomina
#class TestPayroll(models.Model):
#    employee = models.ForeignKey(Employee, verbose_name="Empleado:", on_delete=models.PROTECT, null=True, blank=True)
#    period = models.ForeignKey(Period, on_delete=models.CASCADE)
#    category = models.OneToOneField(CategoryTab, verbose_name="Categoría del puesto:", on_delete=models.CASCADE, related_name='test_category')
#    attribute = models.ForeignKey(AttributeCatalog, on_delete=models.PROTECT, related_name='test_concepts')
#    value     = models.DecimalField("Valor", max_digits=12, decimal_places=2, default=0)

#    class Meta:
#        indexes = [models.Index(fields=['category']),]

    #class Meta:
    #    unique_together = ('category', 'attribute')
    #    ordering = ('attribute__type', 'attribute__name')

#    def __str__(self):
#        return f"{self.employee} ·{self.category} • {self.attribute}: {self.value}"    
    #type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    #type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)
    #perception = models.ForeignKey(PerceptionCatalog, verbose_name="Percepción:", on_delete=models.PROTECT, null=True, blank=True)
    #perception_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    #deduction = models.ForeignKey(DeductionCatalog, verbose_name="Deducción:", on_delete=models.PROTECT, null=True, blank=True)
    #deduction_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

#Nómina    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    gross_pay = models.DecimalField(max_digits=12, decimal_places=2) #sueldo neto
    perception_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deduction_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #total neto
    generation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nómina de {self.employee.name} para el periodo {self.period}"      