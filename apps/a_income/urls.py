from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("income", income_view, name="income"),
    path("NewPayment/<int:pk>", newPayment, name="incomeNewPayment"),
    path("customerSearch", customerSearch, name="incomeCustomerSearch"),
    path("personType", personType, name="incomePersonType"),
    path("newCustomer/<int:pk>", newCustomer, name="incomeNewCustomer"),
    path("saveCustomer", saveCustomer, name="incomeSaveCustomer"),
    # CATALOGO
    path("catalog", catalog_view, name="income-catalog"),
    path("catalogListCategories", catalogListCategories, name="catalogListCategories"),
    path(
        "catalogListSubcategories",
        catalogListSubcategories,
        name="catalogListSubcategories",
    ),
    path("catalogListConcepts", catalogListConcepts, name="catalogListConcepts"),
    path("catalogNewCategory", catalogNewCategory, name="catalogNewCategory"),
    path("catalogNewSubcategory", catalogNewSubcategory, name="catalogNewSubcategory"),
    path("catalogNewConcept", catalogNewConcept, name="catalogNewConcept"),
    path(
        "catalogEditCategory/<int:pk>", catalogEditCategory, name="catalogEditCategory"
    ),
    path(
        "catalogEditSubcategory/<int:pk>",
        catalogEditSubcategory,
        name="catalogEditSubcategory",
    ),
    path("catalogEditConcept/<int:pk>", catalogEditConcept, name="catalogEditConcept"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
