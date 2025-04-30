from django.contrib import admin
from .models import (Dependence, Position, Type, Movement, TypeEmployee, TypePayroll, Bank, WorkingDay, TypeSalary, TaxRegime,PerceptionCatalog,DeductionCatalog, Employee)
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
admin.site.register(PerceptionCatalog)
admin.site.register(DeductionCatalog)
# TODO: EMPLEADOS
admin.site.register(Employee)