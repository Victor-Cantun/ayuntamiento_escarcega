import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import AttributeCatalog, CategoryAttribute, CategoryTab, Dependence, EmployeeAdjustment, EmployeeTaxtData, EmployeeJobData, Period, Position,Type, Movement, TypeEmployee, TypePayroll, Employee
#? tabulador de salarios
from django.db.models import Sum, Prefetch
#? tabulador de salarios
from .forms import EmployeeForm, EmployeeJobForm, EmployeeTaxForm, PeriodForm
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import Count, Q
# Create your views here.
@login_required
def payroll(request):
    return render(request, "admin/payroll/dashboard/index.html")
@login_required
def payroll_employees_overview(request):
    employees_no = Employee.objects.count()
    active_employees = Employee.objects.filter(status = 'ACTIVO').count()
    inactive_employees = Employee.objects.filter(status = 'INACTIVO').count()
    context = {
        "employees_no":employees_no,
        "active_employees":active_employees,
        "inactive_employees":inactive_employees,
    }
    return render(request,"admin/payroll/dashboard/overview.html",context)
@login_required
def payroll_employees_overview_dependence(request):
    dependences = Dependence.objects.annotate( 
        total_employees = Count('employeejobdata__employee'),
        total_active_employees = Count('employeejobdata__employee',filter = Q(employeejobdata__employee__status = 'ACTIVO')),
        total_inactive_employees = Count('employeejobdata__employee',filter = Q(employeejobdata__employee__status = 'INACTIVO')),
    )
    # Calcular los totales generales
    total_empleados = sum(dep.total_employees for dep in dependences)
    total_activos = sum(dep.total_active_employees for dep in dependences)
    total_inactivos = sum(dep.total_inactive_employees for dep in dependences)
    context = {
        'dependences':dependences,
        'total_employees': total_empleados,
        'total_active_employees': total_activos,
        'total_inactive_employees': total_inactivos,
    }
    return render(request,"admin/payroll/dashboard/overview_dependences.html",context)

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
def payroll_catalogs_categories_tabulator(request):
    categories_tab = CategoryTab.objects.all()
    return render(request, "admin/payroll/catalogs/categories_tab/list.html",{"categories_tab":categories_tab})  
@login_required
def payroll_catalogs_attributes(request):
    attributes = AttributeCatalog.objects.all()
    return render(request, "admin/payroll/catalogs/attributes/list.html",{"attributes":attributes})  

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
    employees = Employee.objects.all().select_related('job_information').order_by('id')[:5]
    active_employees = Employee.objects.filter(status = 'ACTIVO').count()
    inactive_employees = Employee.objects.filter(status = 'INACTIVO').count()
    return render(request, "admin/payroll/employees/list.html",{"employees":employees,"active_employees":active_employees,"inactive_employees":inactive_employees})

@login_required
def payroll_employee_detail(request,pk):
    employee_select = get_object_or_404(Employee, id=pk)
    try:
        tax_information = employee_select.tax_information
    except EmployeeTaxtData.DoesNotExist:
        tax_information = None
    
    try:
        job_information = employee_select.job_information
    except EmployeeJobData.DoesNotExist:
        job_information = None
    try:
        employee_adjustments = employee_select.adjustments
    except EmployeeAdjustment.DoesNotExist:
        employee_adjustments = None
    context = {
        'employee': employee_select,
        'tax_information':tax_information,
        'job_information':job_information,
        'adjustments':employee_adjustments,
        }
    return render(request, "admin/payroll/employees/detail.html",context)    

@login_required
def payroll_employee_edit(request,pk):
    employee_select = get_object_or_404(Employee, id=pk)

    try:
        tax_information = employee_select.tax_information
    except EmployeeTaxtData.DoesNotExist:
        tax_information = None
    
    try:
        job_information = employee_select.job_information
    except EmployeeJobData.DoesNotExist:
        job_information = None

    if request.method == 'POST':
    
        employee_form = EmployeeForm(request.POST, instance=employee_select)
        tax_info_form = EmployeeTaxForm(request.POST, instance=tax_information)
        job_info_form = EmployeeJobForm(request.POST, instance=job_information)

        if employee_form.is_valid() and tax_info_form.is_valid() and job_info_form.is_valid():

            employee = employee_form.save()

            if tax_info_form.cleaned_data:
                tax_info = tax_info_form.save(commit=False)
                tax_info.employee = employee
                tax_info.save()
            else:
                if tax_information:
                    tax_information.delete()

            if job_info_form.cleaned_data:
                job_info = job_info_form.save(commit=False)
                job_info.employee = employee
                #dependencia = job_info_form.cleaned_data['dependence']
                #job_info.dependence_id = dependencia.key
                job_info.position_id = request.POST['position']
                job_info.type_employee_id = request.POST['type_employee']
                job_info.type_payroll_id = request.POST['type_payroll']
                job_info.category_id = request.POST['category']
                job_info.total_salary = request.POST['total_salary']
                job_info.save()
            else:
                if job_information:
                    job_information.delete()

            message = "Información guardada"
            return render(request, "admin/payroll/success.html", {"message": message})
    else:    
        job_information = getattr(employee_select, 'job_information', None)
        tax_information = getattr(employee_select, 'tax_information', None)

        positions = Position.objects.all()
        type_employees = TypeEmployee.objects.all()
        type_payrolls = TypePayroll.objects.all()  

        employee_form = EmployeeForm(instance=employee_select)   
        job_employee_form = EmployeeJobForm(instance=job_information)
        tax_employee_form = EmployeeTaxForm(instance=tax_information)

        context = {
            'employee':employee_select,
            'employee_form':employee_form,
            'job_employee_form':job_employee_form,
            'tax_employee_form':tax_employee_form,
            'positions':positions,
            'type_employees':type_employees,
            'type_payrolls':type_payrolls,
            'job_information':job_information,
        }

        return render(request, "admin/payroll/employees/edit.html",context)
        
@login_required
def payroll_employee_check_total_salary(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            position = data.get('position')
            type_employee = data.get('type_employee')
            type_payroll = data.get('type_payroll')
            #print(position)
            #print(type_employee)
            #print(type_payroll)
            percepciones = list(AttributeCatalog.objects.filter(type=AttributeCatalog.PERCEPTION).order_by('name').values_list('name', flat=True))
            deducciones = list(AttributeCatalog.objects.filter(type=AttributeCatalog.DEDUCTION).order_by('name').values_list('name', flat=True))            
            headers = list(percepciones) + list(deducciones)
            #rows = []
            # prefetch para no hacer N+1 queries
            categoria = CategoryTab.objects.get(position_id=position,type_employee_id=type_employee,type_payroll_id=type_payroll)
            cats = CategoryTab.objects.prefetch_related('attributes__attribute').filter(id=categoria.id)
            #cats = CategoryTab.attributes.all()
            #print(cats.id)
            try:
                conceptos = categoria.attributes.all()
            except CategoryTab.DoesNotExist:
                conceptos = None
            #print("mis conceptos")
            #print(conceptos)
            #category = categoria.id
            # 3. Construir las filas
            rows = []
            for cat in cats:
                # Diccionario { nombre_atributo: valor }
                vals = { a.attribute.name: a.value  for a in cat.attributes.all() }
                # Extraer listas alineadas en el mismo orden de headers
                row_per = [ vals.get(nm, 0) for nm in percepciones ]
                row_ded = [ vals.get(nm, 0) for nm in deducciones ]
                total_per = sum(row_per)
                total_ded = sum(row_ded)
                total_salary = total_per - total_ded               
                # Construir la fila completa
                row = row_per + row_ded
                rows.append(row)
            
            #conceptos = []
            
            #context = {'total_salary':total_salary,'category':category,}
            nuevos_campos_html = f"""<div><label for="id_total_salary" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Salario total:</label>
            <input name="total_salary" value="{total_salary}" type="text" id="id_total_salary" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500" placeholder="John" required />
            </div>
            <div>
            <label for="id_category" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Nivel de la categoría:</label>
            <select name="category" id="id_category" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
                <option selected value="{categoria.id}">{categoria}</option>
            </select>
            </div>
            """ 
            #return HttpResponse(resultado_fila)
            return render(request, 'admin/payroll/employees/extra_inputs.html',{
                'headers': headers,
                'rows': rows,
                'nuevos_campos_html': nuevos_campos_html,
                'concepts':conceptos,
                'total_salary':total_salary,
                'category':categoria
            }) 
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Datos JSON inválidos')
        except Exception as e:
            return HttpResponseServerError(f'Error interno del servidor: {e}')

# TODO: PRENOMINA
@login_required
def payroll_test(request):
    return render(request, "admin/payroll/payroll_test/index.html")
@login_required
def payroll_test_periods(request):
    periods = Period.objects.all()
    return render(request, "admin/payroll/payroll_test/list.html",{"periods":periods})
@login_required
def payroll_test_period_new(request):
    if request.method == "POST":
        form = PeriodForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTestPayrollList"
            return response
    else:
        form = PeriodForm()
        return render(request, "admin/payroll/payroll_test/new.html",{"form":form})