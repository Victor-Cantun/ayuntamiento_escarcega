from django.contrib import admin
from .models import (AttributeCatalog, CategoryAttribute, CategoryTab, Dependence, EmployeeAdjustment, EmployeeTaxData, EmployeeJobData, Period, Position, Type, Movement, TypeEmployee, TypePayroll, Bank, WorkingDay, TypeSalary, TaxRegime, Employee)
# Register your models here.
# TODO: CATÁLOGOS
admin.site.register(Dependence)
admin.site.register(Position)
admin.site.register(Type)
admin.site.register(Movement)
admin.site.register(TypeEmployee)
admin.site.register(TypePayroll)
admin.site.register(Bank)
admin.site.register(WorkingDay)
admin.site.register(TypeSalary)
admin.site.register(TaxRegime)
#admin.site.register(PerceptionCatalog)
#admin.site.register(DeductionCatalog)
admin.site.register(AttributeCatalog)
admin.site.register(CategoryAttribute)
# TODO: TABULADORES
admin.site.register(CategoryTab)
#admin.site.register(PerceptionTab)
#admin.site.register(DeductionTab)
# TODO: EMPLEADOS
#admin.site.register(Employee)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('key','paternal_surname', 'maternal_surname', 'name')  # Campos a mostrar en la lista
    search_fields = ('key','paternal_surname', 'maternal_surname', 'name')  # Campos en los que se buscará

class EmpleadoInfoFinanciera(admin.ModelAdmin):
    list_display  = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos a mostrar en la lista
    search_fields = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos en los que se buscará

class EmpleadoInfoLaboral(admin.ModelAdmin):
    list_display  = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos a mostrar en la lista
    search_fields = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos en los que se buscará 

class EmpleadoAjustes(admin.ModelAdmin):
    list_display  = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos a mostrar en la lista
    search_fields = ('employee__key','employee__paternal_surname', 'employee__maternal_surname', 'employee__name')  # Campos en los que se buscará

admin.site.register(Employee, EmpleadoAdmin)
admin.site.register(EmployeeTaxData, EmpleadoInfoFinanciera)
admin.site.register(EmployeeJobData, EmpleadoInfoLaboral)
admin.site.register(EmployeeAdjustment, EmpleadoAjustes)
# TODO: PRENOMINA
admin.site.register(Period)