import json
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Concept, CategoryConcept, Category, Dependence, EmployeeAdjustment, EmployeeCategory, PayrollPeriod, PayrollTest, Position,Type, Movement, TypeEmployee, TypePayroll, Employee
#? tabulador de salarios
from django.db.models import Sum, Prefetch
#? tabulador de salarios
from django.shortcuts import get_object_or_404
from django.forms import inlineformset_factory
from django.db.models import Count, Q
from .forms import AdjustmentFormSet, ConceptCategoryForm, ConceptForm, EmployeeAdjustmentForm, EmployeeCategoryForm, EmployeeForm, SalaryTabulatorForm
from .forms import PayrollDependenceForm, PayrollPositionForm, PayrollTypeForm, PayrollMovementForm, PayrollTypeEmployeeForm, PayrollTypePayrollForm,CategoryForm, PeriodForm
#paginator
from django.http import JsonResponse
from django.core.paginator import Paginator
#from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
#import json
#manejo de errores
from django.contrib import messages
from django.db.models import ProtectedError
# Create your views here.
from django.views import View
from django.db.models import Q, Case, When, Sum, DecimalField
from django.db.models import Sum
from collections import defaultdict
from decimal import Decimal
# TODO: PANEL
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

# Ramos - Dependencias - Direcciones
@login_required
def payroll_catalogs_dependences(request):
    dependences = Dependence.objects.all()
    return render(request, "admin/payroll/catalogs/dependences/list.html",{"dependences":dependences})

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
            context = {
                "message":"Existen errores en el formulario",
                "dependence_form":dependence_form
            }
            return render(request, "admin/payroll/catalogs/dependences/new.html",context)
    else:
        dependence_form = PayrollDependenceForm()
        return render(request, "admin/payroll/catalogs/dependences/new.html",{"dependence_form":dependence_form})    

@login_required
def payroll_catalogs_dependences_edit(request, pk):
    model = get_object_or_404(Dependence,key=pk)
    if request.method == "POST":
        dependence_form = PayrollDependenceForm(request.POST or None, request.FILES or None, instance=model)
        if dependence_form.is_valid()  and request.POST:
            dependence_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateDependencesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "dependence_form":dependence_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/dependences/edit.html",context)    
    else:
        dependence_form = PayrollDependenceForm(instance=model)
        context = {
            "dependence_form":dependence_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/dependences/edit.html",context)    

@login_required
def payroll_catalogs_dependences_delete(request, pk):
    model = get_object_or_404(Dependence, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la Dependencia "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/dependences/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/dependences/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

# Categorias - Puestos - Posiciones 
@login_required
def payroll_catalogs_positions(request):
    positions = Position.objects.all()
    return render(request, "admin/payroll/catalogs/positions/list.html",{"positions":positions})

@login_required
def payroll_catalogs_positions_new(request):
    if request.method == "POST":
        position_form = PayrollPositionForm(request.POST or None, request.FILES or None)
        if position_form.is_valid():
            position_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdatePositionsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "position_form":position_form
            }
            return render(request, "admin/payroll/catalogs/positions/new.html",context)
    else:
        position_form = PayrollPositionForm()
        return render(request, "admin/payroll/catalogs/positions/new.html",{"position_form":position_form}) 

@login_required
def payroll_catalogs_positions_edit(request, pk):
    model = get_object_or_404(Position,key=pk)
    if request.method == "POST":
        position_form = PayrollPositionForm(request.POST or None, request.FILES or None, instance=model)
        if position_form.is_valid()  and request.POST:
            position_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdatePositionsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "position_form":position_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/positions/edit.html",context)    
    else:
        position_form = PayrollPositionForm(instance=model)
        context = {
            "position_form":position_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/positions/edit.html",context)    

@login_required
def payroll_catalogs_positions_delete(request, pk):
    model = get_object_or_404(Position, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la posición "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/positions/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/positions/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#Tipos
@login_required
def payroll_catalogs_types(request):
    types = Type.objects.all()
    return render(request, "admin/payroll/catalogs/types/list.html",{"types":types})

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
            context = {
                "message":"Existen errores en el formulario",
                "type_form":type_form
            }
            return render(request, "admin/payroll/catalogs/types/new.html",context)
    else:
        type_form = PayrollTypeForm()
        return render(request, "admin/payroll/catalogs/types/new.html",{"type_form":type_form})    
    
@login_required
def payroll_catalogs_types_edit(request, pk):
    model = get_object_or_404(Type,key=pk)
    if request.method == "POST":
        type_form = PayrollTypeForm(request.POST or None, request.FILES or None, instance=model)
        if type_form.is_valid()  and request.POST:
            type_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "type_form":type_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/types/edit.html",context)    
    else:
        type_form = PayrollTypeForm(instance=model)
        context = {
            "type_form":type_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/types/edit.html",context)    

@login_required
def payroll_catalogs_types_delete(request, pk):
    model = get_object_or_404(Type, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la tipo "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/types/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/types/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#Cambios/Movimientos
@login_required
def payroll_catalogs_movements(request):
    movements = Movement.objects.all()
    return render(request, "admin/payroll/catalogs/movements/list.html",{"movements":movements})

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
            context = {
                "message":"Existen errores en el formulario",
                "movement_form":movement_form
            }
            return render(request, "admin/payroll/catalogs/movements/new.html",context)
    else:
        movement_form = PayrollMovementForm()
        return render(request, "admin/payroll/catalogs/movements/new.html",{"movement_form":movement_form})   

@login_required
def payroll_catalogs_movements_edit(request, pk):
    model = get_object_or_404(Movement,key=pk)
    if request.method == "POST":
        movement_form = PayrollMovementForm(request.POST or None, request.FILES or None, instance=model)
        if movement_form.is_valid()  and request.POST:
            movement_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateMovementsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "movement_form":movement_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/movements/edit.html",context)    
    else:
        movement_form = PayrollMovementForm(instance=model)
        context = {
            "movement_form":movement_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/movements/edit.html",context)   

@login_required
def payroll_catalogs_movements_delete(request, pk):
    model = get_object_or_404(Movement, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la tipo "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/movements/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/movements/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#Tipo de empleado / sindicato
@login_required
def payroll_catalogs_types_employees(request):
    types_employees = TypeEmployee.objects.all()
    return render(request, "admin/payroll/catalogs/types_employees/list.html",{"types_employees":types_employees})

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
            context = {
                "message":"Existen errores en el formulario",
                "type_employee_form":type_employee_form
            }
            return render(request, "admin/payroll/catalogs/types_employees/new.html",context)
    else:
        type_employee_form = PayrollTypeEmployeeForm()
        return render(request, "admin/payroll/catalogs/types_employees/new.html",{"type_employee_form":type_employee_form})  

@login_required
def payroll_catalogs_types_employees_edit(request, pk):
    model = get_object_or_404(TypeEmployee,key=pk)
    if request.method == "POST":
        type_employee_form = PayrollTypeEmployeeForm(request.POST or None, request.FILES or None, instance=model)
        if type_employee_form.is_valid()  and request.POST:
            type_employee_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesEmployeesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "type_employee_form":type_employee_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/types_employees/edit.html",context)    
    else:
        type_employee_form = PayrollTypeEmployeeForm(instance=model)
        context = {
            "type_employee_form":type_employee_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/types_employees/edit.html",context)   

@login_required
def payroll_catalogs_types_employees_delete(request, pk):
    model = get_object_or_404(TypeEmployee, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la tipo "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/types_employees/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/types_employees/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#Tipo de nomina / nomina
@login_required
def payroll_catalogs_types_payrolls(request):
    types_payrolls = TypePayroll.objects.all()
    return render(request, "admin/payroll/catalogs/types_payrolls/list.html",{"types_payrolls":types_payrolls})

@login_required    
def payroll_catalogs_types_payrolls_new(request):
    if request.method == "POST":
        type_payroll_form = PayrollTypePayrollForm(request.POST or None, request.FILES or None)
        if type_payroll_form.is_valid():
            type_payroll_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesPayrollsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "type_payroll_form":type_payroll_form
            }
            return render(request, "admin/payroll/catalogs/types_payrolls/new.html",context)
    else:
        type_payroll_form = PayrollTypePayrollForm()
        return render(request, "admin/payroll/catalogs/types_payrolls/new.html",{"type_payroll_form":type_payroll_form})  

@login_required
def payroll_catalogs_types_payrolls_edit(request, pk):
    model = get_object_or_404(TypePayroll,key=pk)
    if request.method == "POST":
        type_payroll_form = PayrollTypePayrollForm(request.POST or None, request.FILES or None, instance=model)
        if type_payroll_form.is_valid()  and request.POST:
            type_payroll_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateTypesPayrollsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "type_payroll_form":type_payroll_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/types_payrolls/edit.html",context)    
    else:
        type_payroll_form = PayrollTypePayrollForm(instance=model)
        context = {
            "type_payroll_form":type_payroll_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/types_payrolls/edit.html",context)   

@login_required
def payroll_catalogs_types_payrolls_delete(request, pk):
    model = get_object_or_404(TypePayroll, key=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la tipo "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/types_payrolls/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/types_payrolls/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#CONCEPTOS (Percepciones y Deducciones)
@login_required
def payroll_catalogs_concepts(request):
    concepts = Concept.objects.all()
    return render(request, "admin/payroll/catalogs/concepts/list.html",{"concepts":concepts}) 

@login_required
def payroll_catalogs_concepts_new(request):        
    if request.method == "POST":
        concept_form = ConceptForm(request.POST or None, request.FILES or None)
        if  concept_form.is_valid():
            concept_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateConceptsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "dependence_form":concept_form                
            }
            return render(request, "admin/payroll/catalogs/concepts/new.html",context)
    else:
        concept_form = ConceptForm()
        return render(request, "admin/payroll/catalogs/concepts/new.html",{ "concept_form":concept_form})

@login_required
def payroll_catalogs_concepts_edit(request, pk):
    #print("id:",pk)
    model = get_object_or_404(Concept,id=pk)
    #print(model)
    if request.method == "POST":
        concept_form = ConceptForm(request.POST or None, request.FILES or None, instance=model)
        if concept_form.is_valid()  and request.POST:
            concept_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateConceptsList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "concept_form":concept_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/concepts/edit.html",context)    
    else:
        concept_form = ConceptForm(instance=model)
        context = {
            "concept_form":concept_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/concepts/edit.html",context)   

@login_required
def payroll_catalogs_concepts_delete(request, pk):
    model = get_object_or_404(Concept, id=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la tipo "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/concepts/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/concepts/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

#Categorías
@login_required
def payroll_catalogs_categories(request):
    categories = Category.objects.all()
    return render(request, "admin/payroll/catalogs/categories/list.html",{"categories":categories})  

@login_required
def payroll_catalogs_categories_new(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST or None)
        if category_form.is_valid():
            category_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario", 
                "category_form":category_form,
            }
            return render(request,"admin/payroll/catalogs/categories/new.html",context)
    else:
        category_form = CategoryForm()
        context = {
            "category_form":category_form
        }
        return render(request,"admin/payroll/catalogs/categories/new.html",context)

@login_required
def payroll_catalogs_categories_edit(request,pk):
    model = get_object_or_404(Category,id=pk)
    if request.method == "POST":
        category_form = CategoryForm(request.POST or None, request.FILES or None, instance=model)
        if category_form.is_valid()  and request.POST:
            category_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateCategoriesList"
            return response
        else:
            context = {
                "message":"Existen errores en el formulario",
                "category_form":category_form,
                "model":model,
            }            
            return render(request,"admin/payroll/catalogs/categories/edit.html",context)    
    else:
        category_form = CategoryForm(instance=model)
        context = {
            "category_form":category_form,
            "model":model,
        }
    return render(request,"admin/payroll/catalogs/categories/edit.html",context)  

@login_required
def payroll_catalogs_categories_delete(request,pk):
    model = get_object_or_404(Category, id=pk)
    if request.method == "DELETE":
        try:
            model.delete()
            return HttpResponse("")
        except ProtectedError as e:
            # Puedes obtener los objetos relacionados que impiden la eliminación
            #objetos_relacionados = list(e.protected_objects)
            #nombres_relacionados = ", ".join([str(obj) for obj in objetos_relacionados])
            # Mensaje al usuario
            message = (f'No se pudo eliminar la Categoría "{model.name}" ' 
            f'porque existen registros asociados. ')
            response =  render(request, 'admin/payroll/catalogs/categories/delete.html',{"message":message}) # Redirige al detalle o a la misma página
            #response["HX-Trigger"] = "UpdateDependencesList"
            return HttpResponse(response)
    else:
        response = render(request,"admin/payroll/catalogs/categories/delete.html",{"model":model})
    #    response["HX-Trigger"] = "UpdateDependenceList"
        return HttpResponse(response)

@login_required
def payroll_catalogs_category_detail(request, pk):
    category_select = get_object_or_404(Category, id=pk)
    #? obtener todos las registros relacionados a la categoría seleccionada
    #conceptos = category_select.attributes.all()
    #print(conceptos)
        
    perceptions = CategoryConcept.objects.filter(category = category_select.id, concept__type='P')
    deductions = CategoryConcept.objects.filter(category = category_select.id, concept__type='D')

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

    return render(request, "admin/payroll/catalogs/categories/detail.html",context) 

#Salarios
@login_required
def payroll_salaries(request):
    return render(request,"admin/payroll/salaries/index.html")

@login_required
def payroll_salaries_list(request):
    # 1. Obtener nombres de atributos según tipo
    percepciones = list(Concept.objects.filter(type=Concept.PERCEPTION).order_by('name').values_list('name', flat=True))
    deducciones = list(Concept.objects.filter(type=Concept.DEDUCTION).order_by('name').values_list('name', flat=True))
    #todos = list(Concept.objects.order_by('type','name').values_list('name', flat=True))  
    # 2. Encabezados de la tabla
    headers = ['cve'] + ['Categoría'] +  list(percepciones) + list(deducciones) + ['Total']  + ['Acciones']
    # 3. Construir las filas
    rows = []
    # prefetch para no hacer N+1 queries
    cats = Category.objects.prefetch_related('concepts__concept').order_by('id')
    for cat in cats:
        # Diccionario { nombre_atributo: valor }
        vals = { a.concept.name: a.value for a in cat.concepts.all() }
        # Extraer listas alineadas en el mismo orden de headers
        row_per = [ vals.get(nm, 0) for nm in percepciones ]
        row_ded = [ vals.get(nm, 0) for nm in deducciones ]
        # Agrega formato moneda       
        row_per_form = [ "${:,.2f}".format(vals.get(nm, 0)) for nm in percepciones ]
        row_dec_form = [ "${:,.2f}".format(vals.get(nm, 0)) for nm in deducciones ] 

        total_per = sum(row_per)
        total_ded = sum(row_ded)
        total     = "${:,.2f}".format( total_per - total_ded )
        acciones = f"""
                    <div class="flex space-x-2">
                        <button onclick="AddConcept('{cat.id}')" 
                                class="text-green-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-plus"></i> Agregar
                        </button>
                        <button onclick="CategoryDetail('{cat.id}')" 
                                class="text-blue-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-eye"></i> Detalle
                        </button>                        
                    </div>
                """
        # Construir la fila completa
        row =[str(cat.position_id)] + [str(cat)] + row_per_form + row_dec_form + [total] + [acciones]
        
        rows.append(row)

    return render(request, 'admin/payroll/salaries/list.html',{
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

@login_required
def payroll_employees_list(request):
    return render(request,"admin/payroll/employees/list2.html")

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
        columns = ['key', 'name', 'paternal_surname', 'maternal_surname', 'dependence','position','status','acciones']
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
                #Q(dependence__icontains=search_value) |
                #Q(position__icontains=search_value) |
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
                'dependencia':empleado.dependence.name,
                'posicion':empleado.position.name,                
                'estado': status,
                'acciones': f"""
                    <div class="flex space-x-2">
                        <button onclick="EmployeeDetail('{empleado.key}')" 
                                class="text-gray-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button onclick="EmployeeEdit('{empleado.key}')" 
                                class="text-blue-600 hover:text-blue-900 font-medium">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button onclick="eliminarEmpleado({empleado.key})" 
                                class="text-red-600 hover:text-red-900 font-medium">
                            <i class="fas fa-trash"></i>
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
def payroll_employees_detail(request,pk):
    employee_select = get_object_or_404(Employee, key=pk)
    category = Category.objects.get(position_id = employee_select.position_id, type_employee_id=employee_select.type_employee_id,type_payroll_id = employee_select.type_payroll_id)
    #print(employee_select)
    #print(category.id)
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
def payroll_employees_edit(request,pk):
    employee = get_object_or_404(Employee,key=pk)
    if request.method == "POST":
        name = request.POST.get('name')
        paternal = request.POST.get('paternal_surname')
        maternal = request.POST.get('maternal_surname')
        #print("entre al post")
        employee_form = EmployeeForm(request.POST or None, request.FILES or None, instance = employee)
        #Obtener categoría
        puesto = request.POST.get('position')
        tipo_empleado = request.POST.get('type_employee')
        tipo_nomina = request.POST.get('type_payroll')
        print("name:",name)
        print("Paterno:",paternal)
        print("Materno:",maternal)
        print("Puesto:",puesto)
        print("T empleado:",tipo_empleado)
        print("T nomina:",tipo_nomina)
        category = Category.objects.get(
            position_id = puesto,
            type_employee_id = tipo_empleado, 
            type_payroll_id = tipo_nomina)
        #print("Categoria",category)
        #Obtener conceptos
        category = category   
        perceptions = CategoryConcept.objects.filter(category_id = category, concept__type='P')
        deductions = CategoryConcept.objects.filter(category_id = category, concept__type='D')
        total_perception = sum(item.value for item in perceptions)
        total_deduction = sum(item.value for item in deductions)
        total_salary = total_perception - total_deduction 
        #print("T salary",total_salary)       
        if employee_form.is_valid():
            print("form valido entre a la edición")
            #employee_form.save()
            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateEmployeeList"
            return response
        else:
            #print("form invalido")
            message = "Existen errores en el formulario"
            context = {"message":message,"employee_form":employee_form,"employee":employee}
            return render(request,"admin/payroll/employees/edit.html",context)
    else:
        #print("entre al get")
        employee_form = EmployeeForm(instance = employee)

        #Obtener categoría
        puesto = employee.position
        tipo_empleado = employee.type_employee
        tipo_nomina = employee.type_payroll
        #print("Puesto:",puesto)
        #print("T empleado:",tipo_empleado)
        #print("T nomina:",tipo_nomina)
        category = Category.objects.get(
            position_id = puesto,
            type_employee_id = tipo_empleado, 
            type_payroll_id = tipo_nomina)
        
        emp_category_form = EmployeeCategoryForm(initial={
            "employee":employee.key,
            "category": category.id
        })
        #print("Categoria",category.id)
        #Obtener conceptos
        categoryid = category.id   
        perceptions = CategoryConcept.objects.filter(category_id = categoryid, concept__type='P')
        deductions = CategoryConcept.objects.filter(category_id = categoryid, concept__type='D')
        total_perception = sum(item.value for item in perceptions)
        total_deduction = sum(item.value for item in deductions)
        total_salary = total_perception - total_deduction 
        #print("T perceptions",total_perception)  
        #print("T deductions",total_deduction)  
        #print("T salary",total_salary)  
        ajustesForm = AdjustmentFormSet(instance=employee) 
        categories_all = Category.objects.all()
        context = {
            "employee":employee,
            "categories_all":categories_all,
            "employee_form":employee_form,
            "emp_category_form":emp_category_form,
            "perceptions":perceptions,
            "deductions":deductions,
            "total_perception":total_perception,
            "total_deduction":total_deduction,
            "total_salary":total_salary,
            "category":category,

            "adjustment_formset":ajustesForm,
            }
        return render(request,"admin/payroll/employees/edit.html",context)    

@login_required
def payroll_employee_load_category(request):
    if request.method == 'POST':
        position = request.POST.get('position')
        type_employee = request.POST.get('type_employee')
        type_payroll = request.POST.get('type_payroll')

        print(position)
        print(type_employee)
        print(type_payroll)

        if position and type_employee and type_payroll:
            if position != '' and type_employee != '' and type_payroll != '': 
                try:
                    category = Category.objects.get(position_id=position,type_employee_id=type_employee,type_payroll_id=type_payroll)
                    print(category) 
                    perceptions = CategoryConcept.objects.filter(category = category.id, concept__type='P')
                    deductions = CategoryConcept.objects.filter(category = category.id, concept__type='D')
                    total_perception = sum(item.value for item in perceptions)
                    total_deduction = sum(item.value for item in deductions)
                    total_salary = total_perception - total_deduction

                    return render(request, 'admin/payroll/employees/extra_inputs.html',{
                        'perceptions':perceptions,
                        'deductions':deductions,
                        'total_perception':total_perception,
                        'total_deduction':total_deduction,
                        'total_salary':total_salary,
                        'category':category
                    }) 
                except Category.DoesNotExist:
                    return HttpResponse("")
            return HttpResponse("")
        return HttpResponse("")

# TODO: PRENOMINA
@login_required
def payroll_test(request):
    return render(request, "admin/payroll/payroll_test/index.html")

@login_required
def payroll_test_periods(request):
    periods = PayrollPeriod.objects.all()
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
            context = {
                "message":"Existen errores en el formulario",
                "form":form
            }            
            return render(request, "admin/payroll/payroll_test/new.html",context)
            
    else:
        form = PeriodForm()
        return render(request, "admin/payroll/payroll_test/new.html",{"form":form})
    
@login_required    
def payroll_test_period_edit(request, pk):
    model = get_object_or_404(PayrollPeriod, pk=pk)
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
    model = get_object_or_404(PayrollPeriod, pk=pk)
    model.delete()
    return HttpResponse("")

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
def add_concept_to_category(request,pk):
    category_select = get_object_or_404(Category, id=pk)

    concepts = CategoryConcept.objects.all().filter(category_id = category_select.id ).order_by('-concept__type')
    total_concepts = concepts.count()
    #print(total_concepts)
    #tipos = Concept.objects.values("type").distinct()
    #print(tipos)
    form = ConceptForm()
    context = {
            "category":category_select,
            "form":form,
            "concepts":concepts,
            "total_concepts":total_concepts,
    }
    return render(request, "admin/payroll/catalogs/categories/concept_new.html",context)    

@login_required
def payroll_catalogs_select_concept(request):
    if request.method == "GET":
        type_concept=request.GET["type_concept"]   
        #print(type_concept)
        concepts = Concept.objects.filter(type=type_concept)
        return render(request, "admin/payroll/catalogs/categories/select_concept.html",{"concepts":concepts}) 

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
    concepts = CategoryConcept.objects.all().filter(category_id = category_select.id ).order_by('-concept__type')
    total_concepts = concepts.count()
    #print(total_concepts)
    #tipos = Concept.objects.values("type").distinct()
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
def payroll_catalogs_load_concepts_by_category(request,pk): 
    category_id = pk   
    perceptions = CategoryConcept.objects.filter(category = category_id, concept__type='P')
    deductions = CategoryConcept.objects.filter(category = category_id, concept__type='D')
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

    return render(request, "admin/payroll/catalogs/categories/total_salary.html",context) 

@login_required    
def save_concept_to_category(request):
    if request.method == "POST":
        #category=request.POST["category"]
        #concept=request.POST["attribute"]
        #value = request.POST['value']
        form = SalaryTabulatorForm(request.POST)
        #print(form)
        if form.is_valid():
            #print("entre")
            #instance = form.save(commit=False)
            #instance.category = request.POST.get("category")
            #instance.concept = request.POST.get("concept")
            #instance.value = request.POST.get("value")
            #category = form.cleaned_data["category"]
            #attribute = form.cleaned_data["concept"]
            #value = form.cleaned_data["value"]
            form.save()
            message = "concepto agregado"
            response = render(request, "admin/payroll/catalogs/categories/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateSalaryList"
            return response
        else:
            #print("no entre")
            message = "El concepto ya existe"
            response = render(request, "admin/payroll/catalogs/categories/error.html", {"message": message}) 
            return response

@login_required
def payroll_catalogs_delete_concept_category(request, concept):
    #print(concept)       
    model = get_object_or_404(CategoryConcept, pk=concept)
    if request.method == "DELETE":
        model.delete()
    #return HttpResponse("")
    response = HttpResponse("")
    response["HX-Trigger"] = "UpdateSalaryTabulator"
    return response

@login_required    
def payroll_employees_new(request):
    if request.method == "POST":

        form_emp = EmployeeForm(request.POST)
        category = request.POST.get('category')
        concepts = request.POST.getlist('concepto[]')
        values = request.POST.getlist('valor[]')

        #print(category)
        #print(concepts)
        #print(values)
        #print(form_emp)



        if form_emp.is_valid():
            new_employee = form_emp.save()
            #si existe categoria, se enlaza categoría a empleado
            if category:
                EmployeeCategory.objects.create(
                    employee_id=new_employee.key,
                    category_id=category
                )
            #si existen ajustes, se crean conceptos a empleado
            if concepts and values:
                for i in range(len(concepts)):
                    EmployeeAdjustment.objects.create(
                        employee_id=new_employee.key,
                        concept_id= concepts[i],
                        value = values[i]
                    )

            message = "Registro realizado correctamente"
            response = render(request, "admin/payroll/success.html", {"message": message})
            response["HX-Trigger"] = "update-list"
            return response
        
        else:
            print("error de validacion")
            return render(request, "admin/payroll/employees/new.html", {"employee_form": form_emp})
    else:
        form = EmployeeForm()
        emp_category_form = EmployeeCategoryForm()
        return render(request, "admin/payroll/employees/new.html", {"employee_form": form, "emp_category_form": emp_category_form})
        
@login_required    
def save_concept_to_adjustments(request):
    if request.method == "POST":
        #employee=request.POST["employee"]
        #category=request.POST["category"]
        #concept=request.POST["concept"]
        #value = request.POST['value']
        #print("VISTA GUARDAR")
        #print("eemployee:",employee)
        #print("category:",category)
        #print("concept:",concept)
        #print("value:",value)
        form = EmployeeAdjustmentForm(request.POST)
        if form.is_valid():
            #category = form.cleaned_data["category"]
            #attribute = form.cleaned_data["concept"]
            #value = form.cleaned_data["value"]
            form.save()
            message = "concepto agregado"
            response = render(request, "admin/payroll/catalogs/categories/success.html", {"message": message})
            response["HX-Trigger"] = "UpdateSalaryList"
            return response
        else:
            #print("no entre")
            message = "El concepto ya existe"
            response = render(request, "admin/payroll/catalogs/categories/error.html", {"message": message}) 
            return response
        
@login_required
def payroll_load_adjustments_of_employee(request,pk):
    employee = get_object_or_404(Employee,key=pk)
    #s = employee.adjustments.all()
    emp_category = employee.my_category
    #print("VIISTA CARGAR")
    #print("empleado",employee.key) 
    #print("categoria",emp_category) 
    #print("mis ajustes son:", emp_adjustments)
    #employee_category = EmployeeCategory.objects.get(employee_id = employee.key)
    #print("mi categoria es:",employee.my_category.category)
    #return HttpResponse("")
    perceptions = CategoryConcept.objects.filter(category = emp_category.category, concept__type='P')
    deductions = CategoryConcept.objects.filter(category = emp_category.category, concept__type='D')

    adj_perceptions = EmployeeAdjustment.objects.filter(employee_id = employee.key, concept__type='P')
    adj_deductions = EmployeeAdjustment.objects.filter(employee_id = employee.key, concept__type='D')

    total_perception = sum(item.value for item in perceptions)
    total_deduction = sum(item.value for item in deductions)

    total_adj_perception = sum(item.value for item in adj_perceptions)
    total_adj_deduction = sum(item.value for item in adj_deductions)

    total_salary = (total_perception + total_adj_perception) - (total_deduction + total_adj_deduction)

    context = {
        "perceptions":perceptions, 
        "deductions":deductions,
        "adj_perceptions":adj_perceptions,
        "adj_deductions":adj_deductions,
        "total_perception":total_perception,
        "total_deduction":total_deduction,
        "total_salary":total_salary
    }

    return render(request, "admin/payroll/employees/total_salary.html",context) 

@login_required
def payroll_employees_delete_concept_to_adjustments(request, concept):
    #print(concept)       
    model = get_object_or_404(EmployeeAdjustment, pk=concept)
    if request.method == "DELETE":
        model.delete()
    #return HttpResponse("")
    response = HttpResponse("")
    response["HX-Trigger"] = "UpdateSalaryList"
    return response

@login_required
def payroll_employees_change_category(request):
    employee = request.POST.get('employee')
    id_category = request.POST.get('category')

    print("category:",id_category)
    print("employee:",employee)

    category = get_object_or_404(Category, pk=id_category)

    perceptions = CategoryConcept.objects.filter(category_id = category, concept__type='P')
    deductions = CategoryConcept.objects.filter(category_id = category, concept__type='D')
    total_perception = sum(item.value for item in perceptions)
    total_deduction = sum(item.value for item in deductions)

    adj_perceptions = EmployeeAdjustment.objects.filter(employee_id = employee, concept__type='P')
    adj_deductions = EmployeeAdjustment.objects.filter(employee_id = employee, concept__type='D')

    if adj_perceptions:
        total_adj_perception = sum(item.value for item in adj_perceptions)
    else:
        total_adj_perception = 0
    
    if adj_deductions:
        total_adj_deduction = sum(item.value for item in adj_deductions)
    else:
        total_adj_deduction = 0

    total_salary = (total_perception + total_adj_perception) - (total_deduction + total_adj_deduction) 

    context = {
        "perceptions":perceptions,
        "deductions":deductions,
        "adj_perceptions":adj_perceptions,
        "adj_deductions":adj_deductions,
        "total_perception":total_perception,
        "total_deduction":total_deduction,
        "total_salary":total_salary,
    }    

    return render(request, "admin/payroll/employees/total_salary.html",context)   



@login_required
def payroll_test_process(request,period_id):
    print(period_id)
    context = {
        'periodo': period_id
    }
    id_empleado = 1234
    empleados = Employee.objects.filter(status=True)
    if id_empleado:
        empleado = empleados.get(key=id_empleado)    
        print("empleado",empleado)
        categoria = empleado.my_category.category
        print("cartegoria:",categoria)
        conceptos_x_empleado = CategoryConcept.objects.filter(category_id = categoria.id)
        #print(conceptos_x_empleado)
        conceptos_de_categoria = (item for item in conceptos_x_empleado)
        #print(conceptos_de_categoria)
        ajustes_empleado = EmployeeAdjustment.objects.filter(employee_id=id_empleado)
        conceptos_a_crear=[]
        print("conceptos de categoria")
        for item in conceptos_de_categoria:
           print("concepto: ",item.concept,"valor: ",item.value)
           conceptos_a_crear.append(PayrollTest(period_id= period_id,employee_id = id_empleado,concept_id = item.concept.id,value = item.value))
           
        print("conceptos de ajustes")
        for item in ajustes_empleado:
           print("concepto: ",item.concept,"valor: ",item.value)
           conceptos_a_crear.append(PayrollTest(period_id= period_id,employee_id = id_empleado,concept_id = item.concept.id,value = item.value))
        # Crear conceptos en lote
        if conceptos_a_crear:
            PayrollTest.objects.bulk_create(conceptos_a_crear)
 


    return render(request, "admin/payroll/payroll_test/result_process.html",context)

@login_required
def payroll_test_detail(request,period_id):
    print(period_id)

    id_empleado = 1234
    if id_empleado:
        empleado = Employee.objects.get(key=id_empleado)    
        print("empleado",empleado)


        # Traemos el periodo
        period = PayrollPeriod.objects.get(id=period_id)

        # Traemos todas las percepciones y deducciones
        perceptions = list(Concept.objects.filter(type=Concept.PERCEPTION))
        deductions = list(Concept.objects.filter(type=Concept.DEDUCTION))

        # Traemos todos los registros del periodo
        payroll_data = PayrollTest.objects.filter(period=period)

        # Agrupamos por empleado y concepto
        data_by_employee = defaultdict(dict)

        for item in payroll_data.values(
            'employee__key', 'employee__name', 'concept__id'
        ).annotate(total=Sum('value')):
            emp_key = item['employee__key']
            emp_name = item['employee__name']
            concept_id = item['concept__id']
            total = item['total']
            data_by_employee[emp_key]['name'] = emp_name
            data_by_employee[emp_key][concept_id] = total

        # Calculamos totales por empleado y totales generales por concepto
        employees_data = []
        totals_per_concept = defaultdict(lambda: Decimal('0.00'))
        grand_total = Decimal('0.00')

        for emp_key, concepts in data_by_employee.items():
            total_emp = sum(value for key, value in concepts.items() if key != 'name')
            grand_total += total_emp

            # Sumamos a totales por concepto
            for c_id, val in concepts.items():
                if c_id != 'name':
                    totals_per_concept[c_id] += val

            employees_data.append({
                'key': emp_key,
                'name': concepts['name'],
                'concepts': concepts,
                'total': total_emp
            })

        context = {
            'perceptions': perceptions,
            'deductions': deductions,
            'employees_data': employees_data,
            'totals_per_concept': totals_per_concept,
            'grand_total': grand_total
        }

    return render(request, "admin/payroll/payroll_test/result_process.html",context)    
    