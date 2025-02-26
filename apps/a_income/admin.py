from django.contrib import admin

from apps.a_income.models import (
    Bank,
    BankAccount,
    Customer,
    Category,
    IncomeType,
    Subcategory,
    Concept,
)

# Register your models here.
admin.site.register(Customer)
admin.site.register(IncomeType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Concept)
