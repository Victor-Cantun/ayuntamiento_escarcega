from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Dependence,Category,Type, Movement, TypeEmployee, TypePayroll, Employee
# Create your views here.
@login_required
def payroll(request):
    return render(request, "admin/payroll/index.html")
# ** CATÁLOGOS
@login_required
def payroll_catalogs(request):
    return render(request, "admin/payroll/catalogs/index.html")
@login_required
def payroll_catalogs_dependences(request):
    dependences = Dependence.objects.all()
    return render(request, "admin/payroll/catalogs/dependences/list.html",{"dependences":dependences})
@login_required
def payroll_catalogs_categories(request):
    categories = Category.objects.all()
    return render(request, "admin/payroll/catalogs/categories/list.html",{"categories":categories})
@login_required
def payroll_catalogs_types(request):
    types = Type.objects.all()
    return render(request, "admin/payroll/catalogs/types/list.html",{"types":types})
@login_required
def payroll_catalogs_movements(request):
    movements = Movement.objects.all()
    return render(request, "admin/payroll/catalogs/movements/list.html",{"movements":movements})
@login_required
def payroll_catalogs_types_employees(request):
    types_employees = TypeEmployee.objects.all()
    return render(request, "admin/payroll/catalogs/types_employees/list.html",{"types_employees":types_employees})
@login_required
def payroll_catalogs_types_payrolls(request):
    types_payrolls = TypePayroll.objects.all()
    return render(request, "admin/payroll/catalogs/types_payrolls/list.html",{"types_payrolls":types_payrolls})
# ** EMPLEADOS
@login_required
def payroll_employees(request):
    return render(request, "admin/payroll/employees/index.html")
@login_required
def payroll_employees_list(request):
    employees = Employee.objects.all()
    return render(request, "admin/payroll/employees/list.html",{"employees":employees})