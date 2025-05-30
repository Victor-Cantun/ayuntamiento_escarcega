from django.urls import path
from . import views
urlpatterns = [
# TODO: PENEL    
    path("payroll", views.payroll, name="payroll_admin"),
    path("payroll_employees_overview",views.payroll_employees_overview, name="payroll_employees_overview"),
    path("payroll_employees_overview_dependence",views.payroll_employees_overview_dependence, name="payroll_employees_overview_dependence"),
# TODO: CATÁLOGOS    
    path("payroll_catalogs", views.payroll_catalogs, name="payroll_catalogs"),
    path("payroll_catalogs_dependences", views.payroll_catalogs_dependences, name="payroll_catalogs_dependences"),
    path("payroll_catalogs_dependences_new", views.payroll_catalogs_dependences_new, name="payroll_catalogs_dependences_new"),
    path("payroll_catalogs_categories", views.payroll_catalogs_categories, name="payroll_catalogs_categories"),
    path("payroll_catalogs_categories_new", views.payroll_catalogs_categories_new, name="payroll_catalogs_categories_new"),
    path("payroll_catalogs_types", views.payroll_catalogs_types, name="payroll_catalogs_types"),
    path("payroll_catalogs_types_new", views.payroll_catalogs_types_new, name="payroll_catalogs_types_new"),
    path("payroll_catalogs_movements", views.payroll_catalogs_movements, name="payroll_catalogs_movements"),
    path("payroll_catalogs_movements_new", views.payroll_catalogs_movements_new, name="payroll_catalogs_movements_new"),
    path("payroll_catalogs_types_employees", views.payroll_catalogs_types_employees, name="payroll_catalogs_types_employees"),
    path("payroll_catalogs_types_employees_new", views.payroll_catalogs_types_employees_new, name="payroll_catalogs_types_employees_new"),
    path("payroll_catalogs_types_payrolls", views.payroll_catalogs_types_payrolls, name="payroll_catalogs_types_payrolls"),
    path("payroll_catalogs_types_payrolls_new", views.payroll_catalogs_types_payrolls_new, name="payroll_catalogs_types_payrolls_new"),
    path("payroll_catalogs_categories_tabulator", views.payroll_catalogs_categories_tabulator, name="payroll_catalogs_categories_tabulator"),
    path("payroll_catalogs_categories_tabulator_new", views.payroll_catalogs_categories_tabulator_new, name="payroll_catalogs_categories_tabulator_new"),    
    path("payroll_catalogs_attributes", views.payroll_catalogs_attributes, name="payroll_catalogs_attributes"),
    path("payroll_catalogs_attributes_new", views.payroll_catalogs_attributes_new, name="payroll_catalogs_attributes_new"),
    path("payroll_catalogs_tabulator", views.payroll_catalogs_tabulator, name="payroll_catalogs_tabulator"),
    path("payroll_catalogs_tabulator_new/<int:pk>", views.payroll_catalogs_tabulator_new, name="payroll_catalogs_tabulator_new"),
    path("payroll_catalogs_tabulator_detail/<int:pk>",views.payroll_catalogs_tabulator_detail,name="payroll_catalogs_tabulator_detail"),
    path("payroll_catalogs_select_concept",views.payroll_catalogs_select_concept, name="payroll_catalogs_select_concept"),
    path("payroll_catalogs_add_concept_category",views.payroll_catalogs_add_concept_category,name="payroll_catalogs_add_concept_category"),
    path("payroll_catalogs_load_concepts_category/<int:category>",views.payroll_catalogs_load_concepts_category,name="payroll_catalogs_load_concepts_category"),
    
# TODO: EMPLEADOS    
    path("payroll_employees", views.payroll_employees, name="payroll_employees"),
    path("payroll_employees_list", views.payroll_employees_list, name="payroll_employees_list"),
    path("payroll_employee_detail/<str:pk>", views.payroll_employee_detail, name="payroll_employee_detail"),
    path("payroll_employee_edit/<str:pk>", views.payroll_employee_edit, name="payroll_employee_edit"),
    path("payroll_employee_check_total_salary", views.payroll_employee_check_total_salary, name="payroll_employee_check_total_salary"),
# TODO: PRENOMINA
    path("payroll_test", views.payroll_test, name="payroll_test"),
    path("payroll_test_periods", views.payroll_test_periods, name="payroll_test_periods"),
    path("payroll_test_period_new", views.payroll_test_period_new, name="payroll_test_period_new"),
    path("payroll_test_period_edit/<int:pk>", views.payroll_test_period_edit, name="payroll_test_period_edit"),
    path("payroll_test_period_delete/<int:pk>", views.payroll_test_period_delete, name="payroll_test_period_delete"),    
    ]