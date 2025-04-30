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
        return f"{self.key} - {self.name}"  
    
class Position(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Puesto:", unique=True) 
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"  

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
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
    name = models.CharField(verbose_name="Tipo de empleado:", unique=True) #PENSIONADOS,BASE,SINDICALIZADO....
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('key', 'name') 
    def __str__(self):
        return f"{self.key} - {self.name}"       
    
class TypePayroll(models.Model):
    key = models.CharField(verbose_name="cve", unique=True, primary_key=True)
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
    name = models.CharField(verbose_name="Jornada:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TypeSalary(models.Model):
    name = models.CharField(verbose_name="Tipo de salario:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row     
    
class TaxRegime(models.Model):
    name = models.CharField(verbose_name="Regimen fiscal:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row   
    
#persepciones = sueldo + compensación + despensa + prevesión social multiple

#deducciones = ISR + cuota sindical + deducciones

#total_neto = persepciones - deducciones

class PerceptionCatalog(models.Model):
    name = models.CharField(verbose_name="Nombre de la percepción:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row   
    
class DeductionCatalog(models.Model):
    name = models.CharField(verbose_name="Nombre de la deducción:", unique=True)
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    def __str__(self):
        row = self.name
        return row   

#tabulador de sueldos quincenal
class CategoryTab(models.Model):
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)
    #salary = models.DecimalField(verbose_name="Salario:", max_digits=12, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('position', 'type_employee','type_payroll')
    def __str__(self):
        return f"{self.position}  - {self.type_employee} - {self.type_payroll}"

#Tabulador Quincenal de Percepciones 
class PerceptionTab(models.Model):   
    category = models.ForeignKey(CategoryTab, verbose_name="Categoría del Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    #type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    #type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)     
    perception = models.ForeignKey(PerceptionCatalog, verbose_name="Percepción:", on_delete=models.PROTECT, null=True, blank=True)
    perception_value = models.DecimalField(verbose_name="Valor de la percepción:",max_digits=12, decimal_places=2, default=0.00)
    #deduction = models.ForeignKey(DeductionCatalog, verbose_name="Deducción:", on_delete=models.PROTECT, null=True, blank=True)
    #deduction_value = models.DecimalField(verbose_name="Valor de la Deducción:",max_digits=12, decimal_places=2, default=0.00)
    #class Meta:
    #    unique_together = ('category', 'type_employee','type_payroll')
    def __str__(self):
        return f"{self.category}"

#Tabulador Quincenal de Deducciones
class DeductionTab(models.Model):   
    category = models.ForeignKey(CategoryTab, verbose_name="Categoría del Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    #type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    #type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)     
    deduction = models.ForeignKey(DeductionCatalog, verbose_name="Deducción:", on_delete=models.PROTECT, null=True, blank=True)
    deduction_value = models.DecimalField(verbose_name="Valor de la Deducción:",max_digits=12, decimal_places=2, default=0.00)
    #class Meta:
    #    unique_together = ('category', 'type_employee','type_payroll')        
    def __str__(self):
        return f"{self.category}"



# TODO: EMPLEADOS
class Employee(models.Model): 
    key = models.CharField(verbose_name="cve_empleado", unique=True, primary_key=True)
    paternal_surname = models.CharField(verbose_name="Apellido paterno:", max_length=50, null=True, blank=True)
    maternal_surname = models.CharField(verbose_name="Apellido materno:", max_length=50, null=True, blank=True)            
    name = models.CharField(verbose_name="Nombre:", max_length=100, null=True, blank=True)
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
    sex = [("F", "F"),("M", "M"),]  
    civil_statuses  = [("SOLTERO","SOLTERO"),("CASADO","CASADO"),("DIVORCIADO","DIVORCIADO"),("VIUDO","VIUDO")]
    employee_status = [("ACTIVO","ACTIVO"),("INACTIVO","INACTIVO")]
    sex = models.CharField(verbose_name="Sexo:",choices=sex, null=True, blank=True)    
    marital_status = models.CharField(verbose_name="Estado civil:",choices=civil_statuses, null=True, blank=True)
    status = models.CharField(verbose_name="Estado del empleado:",choices=employee_status, null=True, blank=True)

    def __str__(self):
        return f"{self.paternal_surname} {self.maternal_surname} {self.name}"
    
#datos fiscales
class EmployeeTaxtData(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='tax_information')
    tax_regime = models.ForeignKey(TaxRegime, verbose_name="Régimen fiscal:", on_delete=models.PROTECT, null=True, blank=True)    
    rfc = models.CharField(verbose_name="RFC:", null=True, blank=True)
    curp = models.CharField(verbose_name="CURP:", null=True, blank=True)
    nss = models.CharField(verbose_name="NSS:", null=True, blank=True)
    cp = models.CharField(verbose_name="Código postal:", null=True, blank=True)
    birth_date = models.DateField(verbose_name="Fecha de nacimiento:",blank=True, null=True)

#datos laborales
class EmploymentData(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, primary_key=True, related_name='employment_information')
    dependence = models.ForeignKey(Dependence, verbose_name="Departamento:", on_delete=models.PROTECT, null=True, blank=True)
    position = models.ForeignKey(Position, verbose_name="Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    base_date = models.DateField(verbose_name="Fecha de base:",blank=True, null=True)
    contract_date = models.DateField(verbose_name="Fecha de contrato:",blank=True, null=True)
    contract_termination_date = models.DateField(verbose_name="Fecha de termino de contrato:",blank=True, null=True)
    salary = models.DecimalField(verbose_name="Salario:", max_digits=12, decimal_places=2, default=0.00)
    account_no = models.BigIntegerField(verbose_name="Número de cuenta:", null=True, blank=True)
    bank = models.ForeignKey(Bank, verbose_name="Banco:", on_delete=models.PROTECT, null=True, blank=True)
    chek_in_time = models.TimeField(verbose_name="Hora de entrada", null=True, blank=True)
    chek_out_time = models.TimeField(verbose_name="Hora de salida:", null=True, blank=True)
    working_day = models.ForeignKey(WorkingDay, verbose_name="Jornada:", on_delete=models.PROTECT, null=True, blank=True)
    type_salary = models.ForeignKey(TypeSalary, verbose_name="Tipo de salario:", on_delete=models.PROTECT, null=True, blank=True)  
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)
    category = models.OneToOneField(CategoryTab,verbose_name="Categoría de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    description = models.TextField(verbose_name="Descripción del puesto:", null=True, blank=True) 



#Datos de contacto:
    #Número de teléfono personal
    #Correo electrónico personal
    #Redes sociales (si aplica)

#Historial laboral:
    #Evalúaciones de desempeño
    #Capacitaciones realizadas
    #Cursos de desarrollo profesional
    #Historial de promociones
    #Anotaciones de comportamiento labor

#Datos de nómina:
    #Sueldo base
    #Deducciones (impuestos, seguros, etc.)
    #Pagos adicionales (horas extras, bonificaciones, etc.)
    #Historial de nómina

#Datos de beneficios:
    #Seguro médico
    #Seguro de vida
    #Vacaciones
    #Días de descanso
    #Otros beneficios (planes de retiro, etc.    

#persepciones = sueldo + compensación + despensa + prevesión social multiple

#deducciones = ISR + cuota sindical + deducciones

#total_neto = persepciones - deducciones

#tabulador de sueldos quincenal    
""" class BiweeklySalarySchedule(models.Model):
    category = models.ForeignKey(Category, verbose_name="Puesto:", on_delete=models.PROTECT, null=True, blank=True)
    type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)
    salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #salario
    compensation = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #compensación
    food_pantry = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #despensa
    multiple_social_security = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # previción social multiple
    gross_income = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #persepciones brutas

    income_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) # ISR
    imss_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #cuota IMSS
    union_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #cuota sindical
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #deducciones
    net_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00) #total neto
"""
# TODO: PRENÓMINA

#Periodo de facturación
class Period(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(verbose_name="Descripción:", null=True, blank=True) 
    class Meta:
        unique_together = ('start_date', 'end_date') 
    def __str__(self):
        return f"{self.start_date} - {self.end_date} : {self.description}"

#Prenomina
class TestPayroll(models.Model):
    employee = models.ForeignKey(Employee, verbose_name="Empleado:", on_delete=models.PROTECT, null=True, blank=True)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    category = models.OneToOneField(CategoryTab, verbose_name="Categoría del puesto:", on_delete=models.PROTECT, null=True, blank=True)
    #type_employee = models.ForeignKey(TypeEmployee, verbose_name="Tipo de empleado:", on_delete=models.PROTECT, null=True, blank=True)
    #type_payroll = models.ForeignKey(TypePayroll, verbose_name="Tipo de nómina:", on_delete=models.PROTECT, null=True, blank=True)
    perception = models.ForeignKey(PerceptionCatalog, verbose_name="Percepción:", on_delete=models.PROTECT, null=True, blank=True)
    perception_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deduction = models.ForeignKey(DeductionCatalog, verbose_name="Deducción:", on_delete=models.PROTECT, null=True, blank=True)
    deduction_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
   
    def __str__(self):
        return f"Nómina de {self.employee.name} para el periodo {self.period}"   

#Nómina    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    generation_date = models.DateTimeField(auto_now_add=True)
    perception_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    deduction_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Nómina de {self.employee.name} para el periodo {self.period}"      