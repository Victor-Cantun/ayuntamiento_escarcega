from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
app_name = 'income'
urlpatterns = [
    path("income/facturama", views.consultas_facturama, name="facturama"),
    path("income", views.income_view, name="start"),
    path("income/cash_register/start",views.cash_register_start,name="cash_register_start"),
    path("income/payment/customer/new", views.income_payment_customer_new, name="payment_customer_new"),
    path("income/cash_register/close", views.closing_reigster, name="closing_register"),
    #path("income/payment/customer/save", views.income_payment_customer_save, name="payment_customer_save"),
    #path("income/payment/pay_select_concept", views.income_payment_pay_select_concept, name="pay_select_concept"),
    #path("income/payment/receipt/pdf/<int:receipt_id>",views.income_payment_receipt_pdf,name="receipt_pdf"),
    #? Cliente
    #path("income/payment/customer/person_type", views.income_payment_person_type, name="payment_person_type"),
    path("income/payment/customer/search", views.income_payment_customer_search, name="payment_customer_search"),
    path("income/payment/customer/edit/<int:pk>", views.income_payment_customer_edit, name="payment_customer_edit"),
    path("income/payment/customer/detail/<int:pk>", views.income_payment_customer_detail, name="payment_customer_detail"),
    #? Pago
    path("income/payment/receipt/new/<int:customer_id>", views.income_payment_receipt_new, name="receipt_new"),
    path("income/payment/receipt/save", views.income_payment_receipt_save, name="receipt_save"),
    path("income/payment/concept/search/", views.income_payment_concept_search, name="concept_search"),
    path("income/payment/receipt/detail/<int:pk>",views.income_payment_receipt_detail,name="receipt_detail"),
    path("income/payment/receipt/pdf/<int:receipt_id>",views.income_payment_receipt_pdf,name="payment_receipt_pdf"),
    path("income/payment/invoice/<int:invoice_id>/pdf/",views.income_payment_invoice_pdf,name="invoice_pdf"),
    path("income/payment/invoice/<int:invoice_id>/cencel/",views.income_cancel_invoice,name="cancel_invoice"),
    #? FACTURA
    path('income/xml', views.facturama_xml, name='facturma_xml'),
    path('income/invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('income/invoices/', views.invoice_list, name='invoice_list'),
    #path('income/invoice/new/', views.invoice_create, name='invoice_create'), 
    path('income/invoice/<int:invoice_id>/edit/', views.invoice_edit, name='invoice_edit'), 
    path('income/invoice/<int:invoice_id>/create-cfdi/', views.invoice_create_cfdi, name='invoice_create_cfdi'),
    path('income/invoice/<int:invoice_id>/download-xml/', views.invoice_download_xml, name='invoice_download_xml'),
    path('income/invoice/<int:invoice_id>/download-pdf/', views.invoice_download_pdf, name='invoice_download_pdf'),
    path('income/invoice/<int:invoice_id>/resend-email/', views.invoice_resend_email, name='invoice_resend_email'),
    path('income/invoice/<int:invoice_id>/cancel-cfdi/', views.invoice_cancel_cfdi, name='invoice_cancel_cfdi'), 
    #? Licencias de funcionamiento
    path("income/licenses", views.licenses_view, name="operating_licenses"),
    path("income/license/new", views.license_new, name="license_new"),
    path("income/license/folio/search", views.folio_search, name="folio_search"),
    path("income/license/save", views.license_save, name="license_save"),
    path("income/licenses/list",views.operating_licenses_list,name="operating_licenses_list"),
    path("income/license/pdf/<int:license_id>",views.operating_license_pdf,name="operating_license_pdf"),
    path("validate/license/<str:license_uuid>",views.validate_license,name="validate_license"),
    #? COTIZACIÓN
    path("income/quotations", views.quotations_view, name="quotations"),
    path("income/quotations/list", views.quotations_list, name="quotations_list"),
    path("income/quotations/customer/search", views.quotation_customer_search, name="quotation_customer_search"),
    path("income/quotation/new/<int:customer_id>", views.quotation_new, name="quotation_new"),
    path("income/quotation/save", views.quotation_save, name="quotation_save"),
    path("income/quotation/pdf/<int:quotation_id>",views.income_quotation_pdf,name="quotation_pdf"),
    #TODO: CATALOGO
    path("income/catalog", views.income_catalog_view, name="catalog"),
    #? CATEGORÍA
    path("income/catalog/categories/list", views.income_catalog_categories_list, name="catalog_categories_list"),
    path("income/catalog/category/new", views.income_catalog_category_new, name="catalog_category_new"),
    path("income/catalog/category/edit/<int:pk>", views.income_catalog_category_edit, name="catalog_category_edit"),
    path("income/catalog/category/delete/<int:pk>", views.income_catalog_category_delete, name="catalog_category_delete"),
    #? SUBCATEGORÍA
    path("income/catalog/subcategories/list",views.income_catalog_subcategories_list,name="catalog_subcategories_list"),
    path("income/catalog/subcategory/new", views.income_catalog_subcategory_new, name="catalog_subcategory_new"),
    path("income/catalog/subcategory/edit/<int:pk>",views.income_catalog_subcategory_edit,name="catalog_subcategory_edit"),
    path("income/catalog/subcategory/delete/<int:pk>",views.income_catalog_subcategory_delete,name="catalog_subcategory_delete"),
    #? CONCEPTO
    path("income/catalog/concepts/list", views.income_catalog_concepts_list, name="catalog_concepts_list"),
    path("income/catalog/concept/new", views.income_catalog_concept_new, name="catalog_concept_new"),
    path("income/catalog/concept/edit/<int:pk>", views.income_catalog_concept_edit, name="catalog_concept_edit"),
    path("income/catalog/concept/delete/<int:pk>", views.income_catalog_concept_delete, name="catalog_concept_delete"),
    #TODO: CLIENTES
    path("income/customers", views.income_customers_view, name="customers"),
    path("income/customers/list", views.income_customers_list, name="customers_list"),
    path("income/customers/datatble/", views.customers_datatable, name="customers_datatable"),
    path("income/customer/new", views.income_customer_new, name="customer_new"),
    path("income/customer/edit/<int:pk>", views.income_customer_edit, name="customer_edit"),
    path("income/customer/delete/<int:pk>", views.income_customer_delete, name="customer_delete"),

    path("income/customer/type", views.income_customer_type, name="customer_type"),
    path('income/customer/<int:pk>/edit/', views.income_customer_update, name='customer_update'),
    path("income/customer/save", views.income_customer_save, name="customer_save"),
    path("income/customer/detail/<int:pk>", views.income_customer_detail, name="customer_detail"),

    path('income/customer/physical/',views.person_physical,name="person_physical"),
    path('income/customer/moral/',views.person_moral,name="person_moral"),    
    #TODO: REPORTES
    path("income/reports", views.income_reports_view, name="reports"),
    path("income/reports/list", views.income_reports_list, name="list_of_reports"),
    path("income/reports/types", views.income_reports_types, name="reports_types"),
    path("income/reports/search", views.income_reports_search, name="reports_search"),
    #TODO: BANCOS Y CUENTAS
    path("income/bank_accounts", views.income_bank_accounts_view, name="bank_accounts"),
    #?BANCOS
    path("income/banks/list",views.income_banks_list,name="banks_list"),
    path("income/bank/new",views.income_bank_new,name="bank_new"),
    path("income/bank/edit/<int:pk>",views.income_bank_edit,name="bank_edit"),
    path("income/bank/delete/<int:pk>",views.income_bank_delete,name="bank_delete"),
    #?CUENTAS
    path("income/accounts/list",views.income_accounts_list,name="accounts_list"),
    path("income/account/new",views.income_account_new,name="account_new"),
    path("income/account/edit/<int:pk>",views.income_account_edit,name="account_edit"),
    path("income/account/delete/<int:pk>",views.income_account_delete,name="account_delete"),
    #TODO: PREDIAL
    path("income/predial", views.income_predial_view, name="predial"),
    path("income/predial/list",views.income_predial_list,name="predial_list"),
    path("income/predial/new",views.income_predial_new,name="predial_new"),
    path("income/predial/edit/<int:pk>",views.income_predial_edit,name="predial_edit"),
    path("income/predial/delete/<int:pk>",views.income_predial_delete,name="predial_delete"),
    #TODO: POLIZAS
    path("income/policy", views.income_policy_view, name="policy"),
    path("income/policy/concept/search/", views.income_policy_concept_search, name="policy_concept_search"),
    #? Poliza de Caja
    path("income/policy/cash/list",views.income_cash_policy_list,name="cash_policy_list"),
    path("income/policy/cash",views.cash_policy,name="cash_policy"),
    path("income/policy/cash/new",views.income_cash_policy_new,name="cash_policy_new"),
    path("income/policy/cash/pdf/<int:policy_id>",views.cash_policy_pdf,name="cash_policy_pdf"), 
    path("income/policy/cash/delete/<int:pk>",views.cash_policy_delete,name="cash_policy_delete"),      
    #? Poliza Federal
    path("income/policy/federal/list",views.income_federal_policy_list,name="federal_policy_list"),
    path("income/policy/federal",views.federal_policy,name="federal_policy"),
    path("income/policy/federal/new",views.income_federal_policy_new,name="federal_policy_new"),
    path("income/policy/federal/pdf/<int:policy_id>",views.federal_policy_pdf,name="federal_policy_pdf"),
    path("income/policy/federal/delete/<int:pk>",views.federal_policy_delete,name="federal_policy_delete"),  
    #TODO: STRIPE
    path('payments/concepts', views.concepts_view, name='concepts_view'),
    path("payments/concept/search/", views.payment_concept_search, name="payment_concept_search"),
    path('add-to-cart/<int:concept_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('payments/customer/data',views.payment_customer_data, name='customer_data'),
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
    path('payments/webhook/stripe/', views.stripe_webhook, name='stripe_webhook'),                       
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
