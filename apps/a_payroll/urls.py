from django.urls import path
from . import views
urlpatterns = [
    path("payroll", views.payroll, name="payroll_admin"),
    path("payroll_catalogs", views.payroll_catalogs, name="payroll_catalogs"),
    path("payroll_catalogs_dependences", views.payroll_catalogs_dependences, name="payroll_catalogs_dependences"),
    path("payroll_catalogs_categories", views.payroll_catalogs_categories, name="payroll_catalogs_categories"),
    path("payroll_catalogs_types", views.payroll_catalogs_types, name="payroll_catalogs_types"),
    path("payroll_catalogs_movements", views.payroll_catalogs_movements, name="payroll_catalogs_movements"),
    path("payroll_catalogs_employees", views.payroll_catalogs_types_employees, name="payroll_catalogs_types_employees"),
    path("payroll_catalogs_payrolls", views.payroll_catalogs_types_payrolls, name="payroll_catalogs_types_payrolls"),
    path("payroll_catalogs_perceptions", views.payroll_catalogs_perceptions, name="payroll_catalogs_perceptions"),
    path("payroll_catalogs_deductions", views.payroll_catalogs_deductions, name="payroll_catalogs_deductions"),
    path("payroll_catalogs_categories_tabulator", views.payroll_catalogs_categories_tabulator, name="payroll_catalogs_categories_tabulator"),
    #path("payroll_catalogs_perceptions_tabulator", views.payroll_catalogs_perceptions_tabulator, name="payroll_catalogs_perceptions_tabulator"),
    #path("payroll_catalogs_deductions_tabulator", views.payroll_catalogs_deductions_tabulator, name="payroll_catalogs_deductions_tabulator"),
    #path("payroll_catalogs_salaries_tabulator", views.payroll_catalogs_salaries_tabulator, name="payroll_catalogs_salaries_tabulator"),
    path("payroll_catalogs_attributes", views.payroll_catalogs_attributes, name="payroll_catalogs_attributes"),
    path("payroll_catalogs_tabulator", views.payroll_catalogs_tabulator, name="payroll_catalogs_tabulator"),
    path("payroll_employees", views.payroll_employees, name="payroll_employees"),
    path("payroll_employees_list", views.payroll_employees_list, name="payroll_employees_list"),
    ]