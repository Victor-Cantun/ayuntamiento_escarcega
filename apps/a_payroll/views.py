from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import DeductionCatalog, Dependence,Position, PerceptionCatalog,Type, Movement, TypeEmployee, TypePayroll, Employee
# Create your views here.
@login_required
def payroll(request):
    return render(request, "admin/payroll/index.html")
# TODO: CATÁLOGOS
@login_required
def payroll_catalogs(request):
    return render(request, "admin/payroll/catalogs/index.html")
@login_required
def payroll_catalogs_dependences(request):
    dependences = Dependence.objects.all()
    return render(request, "admin/payroll/catalogs/dependences/list.html",{"dependences":dependences})
@login_required
def payroll_catalogs_categories(request):
    categories = Position.objects.all()
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
@login_required
def payroll_catalogs_perceptions(request):
    perceptions = PerceptionCatalog.objects.all()
    return render(request, "admin/payroll/catalogs/perceptions/list.html",{"perceptions":perceptions})
@login_required
def payroll_catalogs_deductions(request):
    deductions = DeductionCatalog.objects.all()
    return render(request, "admin/payroll/catalogs/deductions/list.html",{"deductions":deductions})    
# TODO: EMPLEADOS
@login_required
def payroll_employees(request):
    return render(request, "admin/payroll/employees/index.html")
@login_required
def payroll_employees_list(request):
    employees = Employee.objects.all()
    return render(request, "admin/payroll/employees/list.html",{"employees":employees})