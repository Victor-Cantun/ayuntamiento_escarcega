from django.contrib import admin

from apps.a_income.models import (
    Bank,
    BankAccount,
    CashRegister,
    CfdiUse,
    Colony,
    Currency,
    Customer,
    Category,
    FiscalRegimen,
    IncomeType,
    PaymentForm,
    PaymentMethod,
    PaymentStatus,
    Subcategory,
    Concept,
    Tax,
    Turn,
    UnitCode,
)

# Register your models here.
admin.site.register(Customer)
admin.site.register(CashRegister)
admin.site.register(IncomeType)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Bank)
admin.site.register(BankAccount)
admin.site.register(Concept)
admin.site.register(PaymentForm)
admin.site.register(PaymentMethod)
admin.site.register(PaymentStatus)
admin.site.register(Currency)
admin.site.register(Colony)
admin.site.register(Turn)
admin.site.register(FiscalRegimen)
admin.site.register(CfdiUse)
admin.site.register(UnitCode)
admin.site.register(Tax)