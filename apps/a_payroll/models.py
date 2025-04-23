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