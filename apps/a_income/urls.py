from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path("income", views.income_view, name="income"),
    path("customer_new/<int:pk>", views.customer_new, name="income_customer_new"),
    path("person_type", views.person_type, name="income_person_type"),
    path("customer_save", views.customer_save, name="income_customer_save"),
    path("customer_search", views.customer_search, name="income_customer_search"),
    path("pay_select_concept", views.pay_select_concept, name="pay_select_concept"),
    path("payment_new/<int:customer_id>", views.payment_new, name="income_payment_new"),
    path("payment_save", views.payment_save, name="income_payment_save"),
    # CATALOGO
    path("catalog", views.catalog_view, name="income-catalog"),
    path("catalogListCategories", views.catalogListCategories, name="catalogListCategories"),
    path("catalogListSubcategories",views.catalogListSubcategories,name="catalogListSubcategories"),
    path("catalogListConcepts", views.catalogListConcepts, name="catalogListConcepts"),
    path("catalogNewCategory", views.catalogNewCategory, name="catalogNewCategory"),
    path("catalogNewSubcategory", views.catalogNewSubcategory, name="catalogNewSubcategory"),
    path("catalogNewConcept", views.catalogNewConcept, name="catalogNewConcept"),
    path("catalogEditCategory/<int:pk>", views.catalogEditCategory, name="catalogEditCategory"),
    path("catalogEditSubcategory/<int:pk>",views.catalogEditSubcategory,name="catalogEditSubcategory"),
    path("catalogEditConcept/<int:pk>", views.catalogEditConcept, name="catalogEditConcept"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
