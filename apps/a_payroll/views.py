from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AttributeCatalog, CategoryAttribute, CategoryTab, DeductionCatalog, Dependence, Position, PerceptionCatalog,Type, Movement, TypeEmployee, TypePayroll, Employee
#? tabulador de salarios
from django.db.models import Sum, Prefetch
#? tabulador de salarios

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
@login_required
def payroll_catalogs_categories_tabulator(request):
    categories_tab = CategoryTab.objects.all()
    return render(request, "admin/payroll/catalogs/categories_tab/list.html",{"categories_tab":categories_tab}) 
#@login_required
#def payroll_catalogs_perceptions_tabulator(request):
#    perceptions_tab = PerceptionTab.objects.all()
#    return render(request, "admin/payroll/catalogs/perceptions_tab/list.html",{"perceptions_tab":perceptions_tab})  
#@login_required
#def payroll_catalogs_deductions_tabulator(request):
#    deductions_tab = DeductionTab.objects.all()
#    return render(request, "admin/payroll/catalogs/deductions_tab/list.html",{"deductions_tab":deductions_tab})   
@login_required
def payroll_catalogs_attributes(request):
    attributes = AttributeCatalog.objects.all()
    return render(request, "admin/payroll/catalogs/attributes/list.html",{"attributes":attributes})  

#@login_required
#def payroll_catalogs_salaries_tabulator(request):
    # 1. Todos los nombres de percepciones y deducciones
    #percepciones = list(PerceptionCatalog.objects.order_by('name').values_list('name', flat=True))
    #deducciones = list(DeductionCatalog.objects.order_by('name').values_list('name', flat=True)) 

    # 2. Encabezados de la tabla
    #headers = ['Categoría'] + percepciones + deducciones

    # 3. Construir las filas
    #rows = []
    #for cat in CategoryTab.objects.order_by('id'):
    #    row = [str(cat)]  # podrías usar cat.id o cat.__str__()

        # Para cada percepción, sumar su valor en esa categoría
    #    for p in percepciones:
    #total_p = (PerceptionTab.objects.filter(category=cat, perception__name=p).aggregate(total=Sum('perception_value'))['total']or 0)row.append(total_p)

        # Para cada deducción, sumar su valor en esa categoría
    #for d in deducciones:
    #total_d = (DeductionTab.objects.filter(category=cat, deduction__name=d).aggregate(total=Sum('deduction_value'))['total']or 0)row.append(total_d)

    #rows.append(row)

    #return render(request, 'admin/payroll/catalogs/salaries_tab/list.html',{'headers': headers,'rows': rows,}) 

@login_required
def payroll_catalogs_tabulator(request):
    # 1. Obtener nombres de atributos según tipo
    percepciones = list(
        AttributeCatalog.objects
            .filter(type=AttributeCatalog.PERCEPTION)
            .order_by('name')
            .values_list('name', flat=True)
    )
    deducciones = list(
        AttributeCatalog.objects
            .filter(type=AttributeCatalog.DEDUCTION)
            .order_by('name')
            .values_list('name', flat=True)
    )
    #todos = list(AttributeCatalog.objects.order_by('type','name').values_list('name', flat=True))  
    # 2. Encabezados de la tabla
    headers = ['Categoría'] +  list(percepciones) + list(deducciones) + ['Total']
    # 3. Construir las filas
    rows = []
    # prefetch para no hacer N+1 queries
    cats = CategoryTab.objects.prefetch_related('attributes__attribute').order_by('id')
    for cat in cats:
        # Diccionario { nombre_atributo: valor }
        vals = { a.attribute.name: a.value for a in cat.attributes.all() }

        # Extraer listas alineadas en el mismo orden de headers
        row_per = [ vals.get(nm, 0) for nm in percepciones ]
        row_ded = [ vals.get(nm, 0) for nm in deducciones ]

        total_per = sum(row_per)
        total_ded = sum(row_ded)
        total     = total_per - total_ded

        # Construir la fila completa
        row = [str(cat)] + row_per + row_ded + [total]
        rows.append(row)

    return render(request, 'admin/payroll/catalogs/salaries_tab/list.html',{
        'headers': headers,
        'rows': rows,
    })           

# TODO: EMPLEADOS
@login_required
def payroll_employees(request):
    return render(request, "admin/payroll/employees/index.html")
@login_required
def payroll_employees_list(request):
    employees = Employee.objects.all()
    return render(request, "admin/payroll/employees/list.html",{"employees":employees})