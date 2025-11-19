from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import OuterRef, Subquery
from apps.a_payroll.models import Employee, Category, EmployeeCategory


class Command(BaseCommand):
    help = 'Sincroniza EmployeeCategory cuando position y payroll coinciden entre Employee y Category'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Iniciando sincronización de EmployeeCategory...'))

        # Subconsulta para obtener la categoría que coincida con position y payroll del empleado
        category_subquery = Category.objects.filter(
            position=OuterRef('position'),
            type_payroll=OuterRef('type_payroll'),
            type_employee=OuterRef('type_employee'),
        ).values('id')[:1]

        # Filtrar empleados que tienen coincidencia con alguna categoría y aún no tienen EmployeeCategory
        employees = Employee.objects.annotate(
            matched_category_id=Subquery(category_subquery)
        ).filter(
            matched_category_id__isnull=False
        ).exclude(
            my_category__isnull=False  # Excluir si ya tienen relación
        )

        total_to_create = employees.count()

        if total_to_create == 0:
            self.stdout.write(self.style.WARNING('No hay registros nuevos para insertar.'))
            return

        # Crear instancias de EmployeeCategory
        employee_category_instances = [
            EmployeeCategory(
                employee=emp,
                category_id=emp.matched_category_id
            )
            for emp in employees
        ]

        # Inserción en bloque
        with transaction.atomic():
            EmployeeCategory.objects.bulk_create(employee_category_instances, batch_size=1000)

        self.stdout.write(self.style.SUCCESS(f'Se crearon {total_to_create} registros en EmployeeCategory.'))
