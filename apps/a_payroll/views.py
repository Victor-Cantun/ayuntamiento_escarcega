import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Concept, CategoryConcept, Category, Dependence, Period, Position,Type, Movement, TypeEmployee, TypePayroll, Employee
#? tabulador de salarios
from django.db.models import Sum, Prefetch
#? tabulador de salarios
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import Count, Q
from .forms import ConceptCategoryForm, ConceptForm, EmployeeForm, SalaryTabulatorForm
from .forms import PayrollDependenceForm, PayrollCategoryForm, PayrollTypeForm, PayrollMovementForm, PayrollTypeEmployeeForm, PayrollTypePayrollForm,CategoryForm, PeriodForm
#paginator
from django.http import JsonResponse
from django.core.paginator import Paginator
#from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
#import json
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
    categories_tab = Category.objects.all()
    return render(request, "admin/payroll/catalogs/categories_tab/list.html",{"categories_tab":categories_tab})  

@login_required
def payroll_catalogs_attributes(request):
    attributes = Concept.objects.all()
    return render(request, "admin/payroll/catalogs/attributes/list.html",{"attributes":attributes})  

@login_required
def payroll_catalogs_tabulator(request):
    # 1. Obtener nombres de atributos según tipo
    percepciones = list(
        Concept.objects
            .filter(type=Concept.PERCEPTION)
            .order_by('name')
            .values_list('name', flat=True)
    )
    deducciones = list(
        Concept.objects
            .filter(type=Concept.DEDUCTION)
            .order_by('name')
            .values_list('name', flat=True)
    )
    #todos = list(Concept.objects.order_by('type','name').values_list('name', flat=True))  
    # 2. Encabezados de la tabla
    headers = ['cve'] + ['Categoría'] +  list(percepciones) + list(deducciones) + ['Total']
    # 3. Construir las filas
    rows = []
    # prefetch para no hacer N+1 queries
    cats = Category.objects.prefetch_related('attributes__attribute').order_by('id')
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
        row =[str(cat.position_id)] + [str(cat)] + row_per + row_ded + [total]
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
def payroll_employees_counter(request):
    active_employees = Employee.objects.filter(status = True).count()
    inactive_employees = Employee.objects.filter(status = False).count()
    total_employees = Employee.objects.all().count()
    context = {
        'active_employees':active_employees,
        'inactive_employees':inactive_employees,
        'total_employees':total_employees,
    }
    return render(request, "admin/payroll/employees/counter.html",context)

@require_http_methods(["POST"])
@csrf_exempt
def empleados_datatable(request):
    """
    Vista AJAX para DataTables con paginación server-side
    Optimizada para manejar grandes volúmenes de datos
    """
    try:
        # Obtener parámetros de DataTables
        draw = int(request.POST.get('draw', 1))
        start = int(request.POST.get('start', 0))
        length = int(request.POST.get('length', 10))
        search_value = request.POST.get('search[value]', '')
        
        # Parámetros de ordenamiento
        order_column_index = int(request.POST.get('order[0][column]', 0))
        order_direction = request.POST.get('order[0][dir]', 'asc')
        
        # Mapeo de columnas para ordenamiento
        columns = ['key', 'name', 'paternal_surname', 'maternal_surname', 'status','acciones']
        order_column = columns[order_column_index] if order_column_index < len(columns) else 'id'
        
        if order_direction == 'desc':
            order_column = f'-{order_column}'
        
        # Query base optimizada con select_related si hay ForeignKeys
        queryset = Employee.objects.all()
        
        # Aplicar filtro de búsqueda si existe
        if search_value:
            queryset = queryset.filter(
                Q(key__icontains=search_value) |
                Q(name__icontains=search_value) |
                Q(paternal_surname__icontains=search_value) |
                Q(maternal_surname__icontains=search_value) |
                Q(status__icontains=search_value) 
            )
        
        # Contar registros totales y filtrados
        total_records = Employee.objects.count()
        filtered_records = queryset.count()
        
        # Aplicar ordenamiento y paginación
        queryset = queryset.order_by(order_column)[start:start + length]
        
        # Construir datos para DataTables
        data = []
        #MyStatus = {item[0]: item[1] for item in Employee.status}
        #print(MyStatus)
        for empleado in queryset:
            status_text = empleado.get_status_display()
            if status_text == 'ACTIVO':
                status = f"""<span class="inline-flex items-center bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-green-900 dark:text-green-300">
                        <span class="w-2 h-2 me-1 bg-green-500 rounded-full"></span>Activo</span> """
            else:
                status = f"""<span class="inline-flex items-center bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full dark:bg-red-900 dark:text-red-300">
                        <span class="w-2 h-2 me-1 bg-red-500 rounded-full"></span>Baja</span> """
            data.append({
                'id': empleado.key,
                'nombre': empleado.name,
                'apellido': empleado.paternal_surname + ' ' + empleado.maternal_surname,                
                'estado': status,
                'acciones': f"""
                    <div class="flex space-x-2">
                        <button onclick="EmployeeDetail('{empleado.key}')" 
                                class="text-gray-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-eye"></i> Detalle
                        </button>
                        <button onclick="editarEmpleado({empleado.key})" 
                                class="text-blue-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button onclick="eliminarEmpleado({empleado.key})" 
                                class="text-red-600 hover:text-red-900 font-medium">
                            <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </div>
                """
            })
        
        # Respuesta para DataTables
        response = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': filtered_records,
            'data': data
        }
        
        return JsonResponse(response)
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'draw': draw if 'draw' in locals() else 1,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': []
        }, status=500)
    


@login_required
def payroll_employee_detail(request,pk):
    employee_select = get_object_or_404(Employee, key=pk)
    category = Category.objects.get(position_id = employee_select.position_id, type_employee_id=employee_select.type_employee_id,type_payroll_id = employee_select.type_payroll_id)
    #print(employee_select)
    print(category.id)
    perceptions = CategoryConcept.objects.filter(category_id = category.id, concept__type='P')
    deductions = CategoryConcept.objects.filter(category_id = category.id, concept__type='D') 
    total_perception = CategoryConcept.objects.filter(category_id = category.id, concept__type='P').aggregate(total=Sum('value'))
    total_deduction = CategoryConcept.objects.filter(category_id = category.id, concept__type='D').aggregate(total=Sum('value')) 
    #print(total_perception['total'])
    #print(total_deduction['total'])
    total_salary = total_perception['total'] - total_deduction['total']
    #print(total_salary)
    context = {
        'employee': employee_select,
        'perceptions':perceptions,
        'deductions':deductions,
        'total_perception':total_perception['total'],
        'total_deduction':total_deduction['total'],
        'total_salary':total_salary,
        }
    return render(request, "admin/payroll/employees/detail.html",context)        

@login_required
def payroll_employee_edit(request,pk):
    pass     

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
            percepciones = list(Concept.objects.filter(type=Concept.PERCEPTION).order_by('name').values_list('name', flat=True))
            deducciones = list(Concept.objects.filter(type=Concept.DEDUCTION).order_by('name').values_list('name', flat=True))            
            headers = list(percepciones) + list(deducciones)
            #rows = []
            # prefetch para no hacer N+1 queries
            categoria = Category.objects.get(position_id=position,type_employee_id=type_employee,type_payroll_id=type_payroll)
            cats = Category.objects.prefetch_related('attributes__attribute').filter(id=categoria.id)
            #cats = Category.attributes.all()
            #print(cats.id)
            try:
                conceptos = categoria.attributes.all()
            except Category.DoesNotExist:
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
    
@login_required    
def payroll_test_period_edit(request, pk):
    model = get_object_or_404(Period, pk=pk)
    if request.method == "POST":
        form = PeriodForm(
            request.POST or None, request.FILES or None, instance=model
        )
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render( request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTestPayrollList"
            return response
    else:
        form = PeriodForm(instance=model)
    return render(request,"admin/payroll/payroll_test/edit.html",{"form": form, "model": model},)    

@login_required    
def payroll_test_period_delete(request, pk):
    model = get_object_or_404(Period, pk=pk)
    model.delete()
    return HttpResponse("")

@login_required
def payroll_catalogs_dependences_new(request):
    if request.method == "POST":
        dependence_form = PayrollDependenceForm(request.POST or None, request.FILES or None)
        if dependence_form.is_valid():
            dependence_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateDependencesList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/dependences/new.html",{"dependence_form":dependence_form})
    else:
        dependence_form = PayrollDependenceForm()
        return render(request, "admin/payroll/catalogs/dependences/new.html",{"dependence_form":dependence_form})    
    
@login_required
def payroll_catalogs_categories_new(request):
    if request.method == "POST":
        position_form = PayrollCategoryForm(request.POST or None, request.FILES or None)
        if position_form.is_valid():
            position_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/categories/new.html",{"position_form":position_form})
    else:
        position_form = PayrollCategoryForm()
        return render(request, "admin/payroll/catalogs/categories/new.html",{"position_form":position_form})
    
@login_required
def payroll_catalogs_types_new(request):
    if request.method == "POST":
        type_form = PayrollTypeForm(request.POST or None, request.FILES or None)
        if type_form.is_valid():
            type_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/types/new.html",{"type_form":type_form})
    else:
        type_form = PayrollTypeForm()
        return render(request, "admin/payroll/catalogs/types/new.html",{"type_form":type_form})    
    
@login_required
def payroll_catalogs_movements_new(request):
    if request.method == "POST":
        movement_form = PayrollMovementForm(request.POST or None, request.FILES or None)
        if movement_form.is_valid():
            movement_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateMovementsList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/movements/new.html",{"movement_form":movement_form})
    else:
        movement_form = PayrollMovementForm()
        return render(request, "admin/payroll/catalogs/movements/new.html",{"movement_form":movement_form})

@login_required
def payroll_catalogs_types_employees_new(request):
    if request.method == "POST":
        type_employee_form = PayrollTypeEmployeeForm(request.POST or None, request.FILES or None)
        if type_employee_form.is_valid():
            type_employee_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesEmployeesList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/types_employees/new.html",{"type_employee_form":type_employee_form})
    else:
        type_employee_form = PayrollTypeEmployeeForm()
        return render(request, "admin/payroll/catalogs/types_employees/new.html",{"type_employee_form":type_employee_form})            

@login_required    
def payroll_catalogs_types_payrolls_new(request):
    if request.method == "POST":
        type_payroll_form = PayrollTypePayrollForm(request.POST or None, request.FILES or None)
        if type_payroll_form.is_valid():
            type_payroll_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesPayrollList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/types_payrolls/new.html",{"type_payroll_form":type_payroll_form})
    else:
        type_payroll_form = PayrollTypePayrollForm()
        return render(request, "admin/payroll/catalogs/types_payrolls/new.html",{"type_payroll_form":type_payroll_form})  

@login_required
def payroll_catalogs_categories_tabulator_new(request):
    if request.method == "POST":
        category_tab_form = CategoryForm(request.POST or None, request.FILES or None)
        if category_tab_form.is_valid():
            category_tab_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCategoriesTabulator"
            return response
        else:
            return render(request, "admin/payroll/catalogs/categories_tab/new.html",{"category_tab_form":category_tab_form})
    else:
        category_tab_form = CategoryForm()
        return render(request, "admin/payroll/catalogs/categories_tab/new.html",{"category_tab_form":category_tab_form}) 

@login_required
def payroll_catalogs_attributes_new(request):        
    if request.method == "POST":
        attribute_catalog_form = ConceptForm(request.POST or None, request.FILES or None)
        if attribute_catalog_form.is_valid():
            attribute_catalog_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateAttributesList"
            return response
        else:
            return render(request, "admin/payroll/catalogs/attributes/new.html",{"attribute_catalog_form":attribute_catalog_form})
    else:
        attribute_catalog_form = ConceptForm()
        return render(request, "admin/payroll/catalogs/attributes/new.html",{"attribute_catalog_form":attribute_catalog_form})  

@login_required
def payroll_catalogs_tabulator_detail(request, pk):
    category_select = get_object_or_404(Category, id=pk)
    #? obtener todos las registros relacionados a la categoría seleccionada
    #conceptos = category_select.attributes.all()
    #print(conceptos)
        
    perceptions = CategoryConcept.objects.filter(category = category_select.id, attribute__type='P')
    deductions = CategoryConcept.objects.filter(category = category_select.id, attribute__type='D')

    total_perception = sum(item.value for item in perceptions)
    total_deduction = sum(item.value for item in deductions)
    total_salary = total_perception - total_deduction
    #print(total_perception)
    #print(total_deduction)
    context = {
        "category":category_select,
        "perceptions":perceptions, 
        "deductions":deductions,
        "total_perception":total_perception,
        "total_deduction":total_deduction,
        "total_salary":total_salary
    }

    return render(request, "admin/payroll/catalogs/categories_tab/detail.html",context)  

@login_required
def payroll_catalogs_select_concept(request):
    if request.method == "GET":
        type_concept=request.GET["type"]   
        #print(type_concept)
        concepts = Concept.objects.filter(type=type_concept)
        return render(request, "admin/payroll/catalogs/categories_tab/select_concept.html",{"concepts":concepts}) 

@login_required
def payroll_catalogs_tabulator_new(request, pk): 
    category_select = get_object_or_404(Category, id=pk)
    #concepts = Concept.objects.all()
    #if request.method == "POST":
        #pass
    #else:
        #perceptions = CategoryConcept.objects.filter(category = category_select.id, attribute__type='P')
        #deductions = CategoryConcept.objects.filter(category = category_select.id, attribute__type='D')

        #total_perception = sum(item.value for item in perceptions)
        #total_deduction = sum(item.value for item in deductions)
        #total_salary = total_perception - total_deduction

        #print(total_perception)
        #print(total_deduction)
    concepts = CategoryConcept.objects.all().filter(category_id = category_select.id ).order_by('-attribute__type')
    total_concepts = concepts.count()
    #print(total_concepts)
    tipos = Concept.objects.values("type").distinct()
    #print(tipos)
    form = ConceptForm()
    context = {
            "category":category_select,
            "form":form,
            "concepts":concepts,
            "total_concepts":total_concepts,
            #"concepts":concepts,
            #"perceptions":perceptions, 
            #"deductions":deductions,
            #"total_perception":total_perception,
            #"total_deduction":total_deduction,
            #"total_salary":total_salary
    }
    return render(request, "admin/payroll/catalogs/categories_tab/new.html",context)           

@login_required    
def payroll_catalogs_add_concept_category(request):
    if request.method == "POST":
        category=request.POST["category"]
        concept=request.POST["attribute"]
        value = request.POST['value']
        print(category)
        print(concept)
        print(value)
        #CategoryConcept.objects.create(category_id=category_id, attribute_id=concept, value=concept_value)
        form = SalaryTabulatorForm(request.POST or None, request.FILES or None)
        #print(form)
        if form.is_valid():
            form.save()
            message = "concepto agregado"
            response = render(request, "admin/payroll/catalogs/categories_tab/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateSalaryTabulator"
            return response
        else:
            message = "El concepto ya existe"
            response = render(request, "admin/payroll/catalogs/categories_tab/error.html", {"message": message})

"""         perceptions = CategoryConcept.objects.filter(category = category, attribute__type='P')
        deductions = CategoryConcept.objects.filter(category = category, attribute__type='D')
        total_perception = sum(item.value for item in perceptions)
        total_deduction = sum(item.value for item in deductions)
        total_salary = total_perception - total_deduction        
        context = {
            "perceptions":perceptions, 
            "deductions":deductions,
            "total_perception":total_perception,
            "total_deduction":total_deduction,
            "total_salary":total_salary,            
        }
        return render(request, "admin/payroll/catalogs/categories_tab/total_salary.html",context)  """

@login_required
def payroll_catalogs_load_concepts_category(request,category): 
    category_id = category   
    perceptions = CategoryConcept.objects.filter(category = category_id, attribute__type='P')
    deductions = CategoryConcept.objects.filter(category = category_id, attribute__type='D')
    total_perception = sum(item.value for item in perceptions)
    total_deduction = sum(item.value for item in deductions)
    total_salary = total_perception - total_deduction

    context = {
        "perceptions":perceptions, 
        "deductions":deductions,
        "total_perception":total_perception,
        "total_deduction":total_deduction,
        "total_salary":total_salary
    }

    return render(request, "admin/payroll/catalogs/categories_tab/total_salary.html",context)  

@login_required
def payroll_catalogs_delete_concept_category(request, concept):
    print(concept)       
    model = get_object_or_404(CategoryConcept, pk=concept)
    if request.method == "DELETE":
        model.delete()
    #return HttpResponse("")
    response = HttpResponse("")
    response["HX-Trigger"] = "UpdateSalaryTabulator"
    return response

@login_required    
def payroll_employee_new(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "update-list"
            return response
        return render(request, "admin/payroll/employees/new.html", {"form": form})
    else:
        form = EmployeeForm()
        return render(request, "admin/payroll/employees/new.html", {"form": form})
        