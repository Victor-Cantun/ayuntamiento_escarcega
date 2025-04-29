from django.contrib import admin
from .models import (Dependence, Category, Type, Movement, TypeEmployee, TypePayroll, Bank, WorkingDay, TypeSalary, TaxRegime, Employee)
# Register your models here.
admin.site.register(Dependence)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Movement)
admin.site.register(TypeEmployee)
admin.site.register(TypePayroll)
admin.site.register(Bank)
admin.site.register(WorkingDay)
admin.site.register(TypeSalary)
admin.site.register(TaxRegime)
admin.site.register(Employee)