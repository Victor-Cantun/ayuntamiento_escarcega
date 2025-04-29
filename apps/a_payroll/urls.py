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
    path("payroll_employees", views.payroll_employees, name="payroll_employees"),
    path("payroll_employees_list", views.payroll_employees_list, name="payroll_employees_list"),
    ]