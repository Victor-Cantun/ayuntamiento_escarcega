from django.urls import path
from . import views
urlpatterns = [
# TODO: PENEL    
    path("payroll", views.payroll, name="payroll_admin"),
    path("payroll_employees_overview",views.payroll_employees_overview, name="payroll_employees_overview"),
    path("payroll_employees_overview_dependence",views.payroll_employees_overview_dependence, name="payroll_employees_overview_dependence"),
# TODO: CATÁLOGOS    
    path("payroll/catalogs", views.payroll_catalogs, name="payroll_catalogs"),
#Dependencias/Ramos/Dirección
    path("payroll/catalogs/dependences", views.payroll_catalogs_dependences, name="payroll_catalogs_dependences"),
    path("payroll/catalogs/dependences/new", views.payroll_catalogs_dependences_new, name="payroll_catalogs_dependences_new"),
    path("payroll/catalogs/dependences/edit/<str:pk>", views.payroll_catalogs_dependences_edit, name="payroll_catalogs_dependences_edit"),
    path("payroll/catalogs/dependences/delete/<str:pk>", views.payroll_catalogs_dependences_delete, name="payroll_catalogs_dependences_delete"),
#Puestos/Categorias/posición/
    path("payroll/catalogs/positions", views.payroll_catalogs_positions, name="payroll_catalogs_positions"),
    path("payroll/catalogs/positions/new", views.payroll_catalogs_positions_new, name="payroll_catalogs_positions_new"),
    path("payroll/catalogs/positions/edit/<str:pk>", views.payroll_catalogs_positions_edit, name="payroll_catalogs_positions_edit"),
    path("payroll/catalogs/positions/delete/<str:pk>", views.payroll_catalogs_positions_delete, name="payroll_catalogs_positions_delete"),
#Tipos
    path("payroll/catalogs/types", views.payroll_catalogs_types, name="payroll_catalogs_types"),
    path("payroll/catalogs/types/new", views.payroll_catalogs_types_new, name="payroll_catalogs_types_new"),
    path("payroll/catalogs/types/edit/<str:pk>", views.payroll_catalogs_types_edit, name="payroll_catalogs_types_edit"),
    path("payroll/catalogs/types/delete/<str:pk>", views.payroll_catalogs_types_delete, name="payroll_catalogs_types_delete"),
#Cambios/Movimientos
    path("payroll/catalogs/movements", views.payroll_catalogs_movements, name="payroll_catalogs_movements"),
    path("payroll/catalogs/movements/new", views.payroll_catalogs_movements_new, name="payroll_catalogs_movements_new"),
    path("payroll/catalogs/movements/edit/<str:pk>", views.payroll_catalogs_movements_edit, name="payroll_catalogs_movements_edit"),
    path("payroll/catalogs/movements/delete/<str:pk>", views.payroll_catalogs_movements_delete, name="payroll_catalogs_movements_delete"),
#Tipo de empleado / sindicato
    path("payroll/catalogs/types/employees", views.payroll_catalogs_types_employees, name="payroll_catalogs_types_employees"),
    path("payroll/catalogs/types/employees/new", views.payroll_catalogs_types_employees_new, name="payroll_catalogs_types_employees_new"),
    path("payroll/catalogs/types/employees/edit/<str:pk>", views.payroll_catalogs_types_employees_edit, name="payroll_catalogs_types_employees_edit"),
    path("payroll/catalogs/types/employees/delete/<str:pk>", views.payroll_catalogs_types_employees_delete, name="payroll_catalogs_types_employees_delete"),
#Tipo de nomina / nomina
    path("payroll/catalogs/types/payrolls", views.payroll_catalogs_types_payrolls, name="payroll_catalogs_types_payrolls"),
    path("payroll/catalogs/types/payrolls/new", views.payroll_catalogs_types_payrolls_new, name="payroll_catalogs_types_payrolls_new"),
    path("payroll/catalogs/types/payrolls/edit/<str:pk>", views.payroll_catalogs_types_payrolls_edit, name="payroll_catalogs_types_payrolls_edit"),
    path("payroll/catalogs/types/payrolls/delete/<str:pk>", views.payroll_catalogs_types_payrolls_delete, name="payroll_catalogs_types_payrolls_delete"),
#?CONCEPTOS (Percepciones y Deducciones)   
    path("payroll/catalogs/concepts", views.payroll_catalogs_concepts, name="payroll_catalogs_concepts"),
    path("payroll/catalogs/concepts/new", views.payroll_catalogs_concepts_new, name="payroll_catalogs_concepts_new"),
    path("payroll/catalogs/concepts/edit/<str:pk>", views.payroll_catalogs_concepts_edit, name="payroll_catalogs_concepts_edit"),
    path("payroll/catalogs/concepts/delete/<str:pk>", views.payroll_catalogs_concepts_delete, name="payroll_catalogs_concepts_delete"),    
#?CATEGORIA (puesto+tipo de empleado + tipo de nomina)
    path("payroll/catalogs/categories", views.payroll_catalogs_categories, name="payroll_catalogs_categories"),
    path("payroll/catalogs/categories/new", views.payroll_catalogs_categories_new, name="payroll_catalogs_categories_new"),
    path("payroll/catalogs/categories/edit/<int:pk>", views.payroll_catalogs_categories_edit, name="payroll_catalogs_categories_edit"),
    path("payroll/catalogs/categories/delete/<int:pk>", views.payroll_catalogs_categories_delete, name="payroll_catalogs_categories_delete"),
    path("payroll/catalogs/categories/detail/<int:pk>", views.payroll_catalogs_category_detail, name="payroll_catalogs_category_detail"),


    #path("payroll/catalogs/categories_tabulator_new", views.payroll_catalogs_categories_tabulator_new, name="payroll_catalogs_categories_tabulator_new"), 

#?TABULADOR DE SUELDOS (CATEGORIA)     
    path("payroll/salaries", views.payroll_salaries, name="payroll_salaries"),
    path("payroll/salaries/list", views.payroll_salaries_list, name="payroll_salaries_list"),
    path("payroll/catalogs/category/concept/new/<int:pk>",views.add_concept_to_category,name="add_concept_to_category"),
    path("payroll/catalogs/select/concept",views.payroll_catalogs_select_concept, name="payroll_catalogs_select_concept"), 
    path("payroll/catalogs/category/load/concepts/<int:pk>",views.payroll_catalogs_load_concepts_by_category,name="payroll_catalogs_load_concepts_by_category"),
    path("payroll/catalogs/category/concept/save",views.save_concept_to_category,name="save_concept_to_category"),
    path("payroll/catalogs/tabulator_new/<int:pk>", views.payroll_catalogs_tabulator_new, name="payroll_catalogs_tabulator_new"),
    #path("payroll_catalogs_tabulator_detail/<int:pk>",views.payroll_catalogs_tabulator_detail,name="payroll_catalogs_tabulator_detail"),    
    path("payroll/catalogs/delete_concept_category/<int:concept>",views.payroll_catalogs_delete_concept_category,name="payroll_catalogs_delete_concept_category"),
# TODO: EMPLEADOS    
    path("payroll/employees", views.payroll_employees, name="payroll_employees"),
    path("payroll/employees/counter", views.payroll_employees_counter, name="payroll_employees_counter"),
    path("payroll/employees/list",views.payroll_employees_list,name="payroll_employees_list"),
    path('payroll/employees/datatable/', views.empleados_datatable, name='empleados_datatable'),
    path('payroll/employees/new',views.payroll_employees_new,name="payroll_employees_new"),
    path("payroll/employees/detail/<str:pk>", views.payroll_employees_detail, name="payroll_employees_detail"),
    path("payroll/employees/edit/<str:pk>", views.payroll_employees_edit, name="payroll_employees_edit"),
    #path("payroll_employees_list/", views.payroll_employees_list, name="payroll_employees_list"),
    path("payroll/employees/load/category", views.payroll_employee_load_category, name="payroll_employee_load_category"),
    path("payroll/employees/change/category",views.payroll_employees_change_category,name="payroll_employees_change_category"),
    path("payroll/employees/adjustments/save/concept",views.save_concept_to_adjustments,name="save_concept_to_adjustments"),
    path("payroll/employees/load/adjustments/<str:pk>",views.payroll_load_adjustments_of_employee,name="payroll_load_adjustments_of_employee"),
    path("payroll/employees/delete/concept/adjustments/<int:concept>",views.payroll_employees_delete_concept_to_adjustments,name="payroll_employees_delete_concept_to_adjustments"),
    
 
# TODO: PERIODOS
    #? periodos
    path("payroll_test", views.payroll_test, name="payroll_test"),
    path("payroll_test_periods", views.payroll_test_periods, name="payroll_test_periods"),
    path("payroll_test_period_new", views.payroll_test_period_new, name="payroll_test_period_new"),
    path("payroll_test_period_edit/<int:pk>", views.payroll_test_period_edit, name="payroll_test_period_edit"),
    path("payroll_test_period_delete/<int:pk>", views.payroll_test_period_delete, name="payroll_test_period_delete"),
    #? prenomina
    path("payroll_test/<int:period_id>/process",views.payroll_test_process, name="payroll_test_process"),
    path("payroll_test/<int:period_id>/detail",views.payroll_test_detail, name="payroll_test_detail")    


    ]