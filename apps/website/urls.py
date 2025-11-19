from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
# TODO-VISTAS PUBLICAS
    # ListarCabildo
    path("listCouncil", views.listCouncil, name="listCouncil"),
    # ListarSlider
    path("listCarousel", views.listCarousel, name="listCarousel"),
    # ListarDependencias
    path("PublicListDependences",views.PublicListDependences,name="PublicListDependences"),
    # SMAPAE
    path("listYearsSMAPAE", views.listYearsSMAPAE, name="listYearsSMAPAE"),
    path("listCategoriesSMAPAE", views.listCategoriesSMAPAE, name="listCategoriesSMAPAE"),
    path("listSubcategoriesSMAPAE/<int:pk>/",views.listSubcategoriesSMAPAE,name="listSubcategoriesSMAPAE"),
    path("listDocumentsSMAPAE/<int:subgrupo>/<int:year>/",views.listDocumentsSMAPAE,name="listDocumentsSMAPAE",),
    # SEVAC-SMAPAE
    path("sevac_listYears", views.sevac_listYears, name="sevac_listYears"),
    path("sevac_listCategories", views.sevac_listCategories, name="sevac_listCategories"),
    path("sevac_listSubcategories/<int:pk>/",views.sevac_listSubcategories,name="sevac_listSubcategories"),
    path("sevac_listDocuments/<int:subgrupo>/<int:year>/",views.sevac_listDocuments,name="sevac_listDocuments",),
    # ListarContabiliidad
    path("listAccounting", views.listAccounting, name="listAccounting"),
    # ListarContabiliidad
    path("listGazette", views.listGazette, name="listGazette"),
    path("listYears", views.listYears, name="listYears"),
    # ListarBlog
    path("listPosts", views.listPosts, name="listPosts"),
    # TRANSPARENCIA
    path("listCategoryTransparency",views.listCategoryTransparency,name="listCategoryTransparency"),
    path("listDocumentsTransparency/<int:category>/<int:dependence>",views.listDocumentsTransparency,name="listDocumentsTransparency"),
    # Obligaciones
    path("listCommonObligations",views.listCommonObligations,name="listCommonObligations",),
    path("listCommonObligationsDocuments/<int:pk>",views.listCommonObligationsDocuments,name="listCommonObligationsDocuments",),
# TODO-VISTAS PRIVADAS
    # ?CARRUSEL
    path("carousel", views.carousel_admin, name="carousel_admin"),
    path("list_carousel", views.list_carousel, name="list_carousel"),
    path("newCarousel", views.newCarousel, name="newCarousel"),
    path("editCarousel", views.editCarousel, name="editCarousel"),
    path("editCarousel/<int:pk>", views.editCarousel, name="editCarousel"),
    path("deleteCarousel/<int:pk>", views.deleteCarousel, name="deleteCarousel"),
    # ?CABILDO
    path("list_council", views.list_council, name="list_council"),
    path("newCouncil", views.newCouncil, name="newCouncil"),
    path("editCouncil", views.editCouncil, name="editCouncil"),
    path("editCouncil/<int:pk>", views.editCouncil, name="editCouncil"),
    path("deleteCouncil/<int:pk>", views.deleteCouncil, name="deleteCouncil"),
    # ?DIRECTOR
    path("list_directors", views.list_directors, name="list_directors"),
    path("new_director", views.new_director, name="new_director"),
    path("edit_director", views.edit_director, name="edit_director"),
    path("edit_director/<int:pk>", views.edit_director, name="edit_director"),
    path("deleteDirector/<int:pk>", views.deleteDirector, name="deleteDirector"),
    # ?DEPENDENCIA
    path("dependences", views.dependences_admin, name="dependences_admin"),
    path("list_dependences", views.list_dependences, name="list_dependences"),
    path("new_dependence", views.new_dependence, name="new_dependence"),
    path("edit_dependence", views.edit_dependence, name="edit_dependence"),
    path("edit_dependence/<int:pk>", views.edit_dependence, name="edit_dependence"),
    path("deleteDependence/<int:pk>", views.deleteDependence, name="deleteDependence"),
    # ?TRANSPARENCIA
    path("listAllDocuments", views.listAllDocuments, name="listAllDocuments"),
    path("list_accounting", views.list_accounting, name="list_accounting"),
    path("newAccounting", views.newAccounting, name="newAccounting"),
    path("editAccounting", views.editAccounting, name="editAccounting"),
    path("editAccounting/<int:pk>", views.editAccounting, name="editAccounting"),
    path("deleteAccounting/<int:pk>", views.deleteAccounting, name="deleteAccounting"),
    # ?GACETA
    path("gazette", views.gazette_admin, name="gazette_admin"),
    path("list_gazette", views.list_gazette, name="list_gazette"),
    path("newGazette", views.newGazette, name="newGazette"),
    path("editGazette", views.editGazette, name="editGazette"),
    path("editGazette/<int:pk>", views.editGazette, name="editGazette"),
    path("deleteGazette/<int:pk>", views.deleteGazette, name="deleteGazette"),
    # ?DOCUMENTO-DRIVE-REPOSITORIO
    path("documents", views.documents_admin, name="documents_admin"),
    path("list_document", views.list_document, name="list_document"),
    path("newDocument", views.newDocument, name="newDocument"),
    path("editDocument", views.editDocument, name="editDocument"),
    path("editDocument/<int:pk>", views.editDocument, name="editDocument"),
    path("deleteDocument/<int:pk>", views.deleteDocument, name="deleteDocument"),
    path("detailDocument/<int:pk>", views.detailDocument, name="detailDocument"),
    path("verDocument/<int:pk>", views.verDocument, name="verDocument"),
    # ?POST-BLOG
    path("list_posts", views.list_posts, name="list_posts"),
    path("newPost", views.newPost, name="newPost"),
    path("editPost", views.editPost, name="editPost"),
    path("editPost/<int:pk>", views.editPost, name="editPost"),
    path("deletePost/<int:pk>", views.deletePost, name="deletePost"),
    # ?GRUPOS
    path("listInfoGroup", views.listInfoGroup, name="listInfoGroup"),
    path("newInfoGroup", views.newInfoGroup, name="newInfoGroup"),
    path("deleteInfoGroup/<int:pk>", views.deleteInfoGroup, name="deleteInfoGroup"),
    path("editInfoGroup/<int:pk>", views.editInfoGroup, name="editInfoGroup"),
    path("selectInfoGroup/<int:pk>", views.selectInfoGroup, name="selectInfoGroup"),
    # ?SUBGRUPOS
    path("listInfoSubgroup", views.listInfoSubgroup, name="listInfoSubgroup"),
    path("newInfoSubgroup", views.newInfoSubgroup, name="newInfoSubgroup"),
    path("deleteInfoSubgroup/<int:pk>",views.deleteInfoSubgroup,name="deleteInfoSubgroup"),
    path("editInfoSubgroup/<int:pk>", views.editInfoSubgroup, name="editInfoSubgroup"),
    path("selectInfoSubgroup/<int:pk>",views.selectInfoSubgroup,name="selectInfoSubgroup"),
    # ?TRANSPARENCIA
    path("transparency", views.transparency, name="transparency"),
    path("newDocumentTransparency",views.newDocumentTransparency,name="newDocumentTransparency"),
    path("listDocumenTransparency",views.listDocumenTransparency,name="listDocumenTransparency"),
    path("deleteDocumentTransparency/<int:pk>",views.deleteDocumentTransparency,name="deleteDocumentTransparency"),
    # ?TRANSPARENCIA-OBLIGACIONES COMUNES
    path("obligation", views.obligation, name="obligation"),
    path("newObligation", views.newObligation, name="newObligation"),
    path("listObligations", views.listObligations, name="listObligations"),
    path("newObligationDocument",views.newObligationDocument,name="newObligationDocument",),
    path("listObligationsDocuments",views.listObligationsDocuments,name="listObligationsDocuments"),
    path("deleObligationteDocument/<int:pk>",views.deleteObligationDocument,name="deleteObligationDocument"),
    # *?CRUD
    path("createPost/", views.CreatePostView.as_view(), name="createPost"),
    path("carousel/", views.carouselListCreateView.as_view(), name="carousel-lc"),
    path("carousel/<int:pk>/",views.carouselUpdateDestroyView.as_view(),name="carousel-rud",),
    path("accounting/", views.accountingListCreateView.as_view(), name="accounting-lc"),
    path("user", views.UserDetail.as_view(), name="user_detail"),
    path("positions/", views.PositionsListCreateView.as_view(), name="positions-lc"),
    path("council/", views.CouncilListCreateView.as_view(), name="council-lc"),
    path("council/<int:pk>/",views.CouncilUpdateDestroyView.as_view(),name="council-rud"),
    path("directors/", views.DirectorsListCreateView.as_view(), name="directors-lc"),
    path("directors/<int:pk>/",views.DirectorsUpdateDestroyView.as_view(),name="directors-rud"),
    path("dependences/", views.DependencesListCreateView.as_view(), name="dependences-lc"),
    path("dependences/<int:pk>/",views.DependencesUpdateDestroyView.as_view(),name="dependences-rud",
    ),
    # ?SMAPAE-transparencia
    path("Accounting", views.Accounting, name="Accounting"),
    path("Accounting/SelectYears", views.select_years, name="select_years"),
    #categorias
    path("Accounting/ListCategories",views.AccountingListCategories,name="AccountingListCategories"),
    path("Accounting/NewCategory",views.AccountingNewCategory,name="AccountingNewCategory"),
    path("Accounting/EditCategory/<int:pk>/",views.AccountingEditCategory,name="AccountingEditCategory"),
    path("Accounting/DetailCategory/<int:pk>/",views.AccountingDetailCategory,name="AccountingDetailCategory"),
    path("Accounting/DeleteCategory/<int:pk>/",views.AccountingDeleteCategory,name="AccountingDeleteCategory"),
    path("Accounting/Subcategories/<int:category_id>/",views.Subcategories,name="Subcategories"),
    path("Accounting/AddSubcategory",views.AddSubcategory,name="AddSubcategory"),

    path('ordenar/', views.ordenar_categorias, name='ordenar_categorias'),
    #path('reordenar/', views.reordenar_tareas, name='reordenar_tareas'),
    path('actualizar-orden/', views.actualizar_orden, name='actualizar_orden'),

    #Subcategorias
    path("Accounting/SelectCategories",views.select_categories,name="select_categories"),
    path("Accounting/ListSubcategoriesForYear/",views.list_subcategories,name="ListSubcategories"),
    path("Accounting/ListSubcategories",views.AccountingListSubcategories,name="AccountingListSubcategories"),
    path("Accounting/NewSubcategory",views.AccountingNewSubcategory,name="AccountingNewSubcategory",),
    path("Accounting/EditSubcategory/<int:pk>/",views.AccountingEditSubcategory,name="AccountingEditSubcategory"),
    path("Accounting/DetailSubcategory/<int:pk>/year/<int:year>",views.AccountingDetailSubcategory,name="AccountingDetailSubcategory"),
    path("Accounting/DeleteSubcategory/<int:pk>/",views.AccountingDeleteSubcategory,name="AccountingDeleteSubcategory"),
    path('ordenar/subcategorias', views.ordenar_subcategorias, name='ordenar_subcategorias'),
    path('actualizar-orden-subcategorias', views.actualizar_orden_subcategorias, name='actualizar_orden_subcategorias'),
    path('Accounting/ListarTrimestres/year/<int:year>/subcategory/<int:pk>', views.ListarTrimestres, name='ListarTrimestres'),
    path('Accounting/DeleteTrimestre/<int:pk>', views.DeleteTrimestre, name='DeleteTrimestre'),
    path('Accounting/CancelDelete', views.CancelDelete, name='CancelDelete'),
    #Documentos
    path("Accounting/NewDocument",views.AccountingNewDocument,name="AccountingNewDocument"),
    path("AccountingListDocuments",views.AccountingListDocuments,name="AccountingListDocuments"),
    path("Accounting/EditDocument/<int:pk>/",views.AccountingEditDocument,name="AccountingEditDocument"),
    path("Accounting/DeleteDocument/<int:pk>/",views.AccountingDeleteDocument,name="AccountingDeleteDocument"),
    

    path("Accounting/SelectCategories",views.AccountingSelectCategories,name="AccountingSelectCategories"),
    path("Accounting/SelectCategoriesInDocuments",views.AccountingSelectCategoriesInDocuments,name="AccountingSelectCategoriesInDocuments"),
    path("Accounting/SelectSubcategories",views.AccountingSelectSubcategories,name="AccountingSelectSubcategories"),
    path("Accounting/ListYearsInDocuments",views.AccountingListYearsInDocuments,name="AccountingListYearsInDocuments"),
    # ?SEVAC
    path("SMAPAE/SEVAC",views.sevac_view,name="sevac"),
    path("SMAPAE/SEVAC/ListCategories",views.sevac_list_categories,name="SevacListCategories"),
    #path("SMAPAE/SEVAC/ListCategories/year/<int:year>",views.sevac_list_categories_for_year,name="SevacListCategoriesForYear"),
    path("SMAPAE/SEVAC/NewCategory",views.sevac_new_category,name="SevacNewCategory"),
    path("SMAPAE/SEVAC/DetailCategory/<int:pk>",views.sevac_detail_category,name="SevacDetailCategory"),
    path("SMAPAE/SEVAC/EditCategory/<int:pk>",views.sevac_edit_category,name="SevacEditCategory"),
    path("SMAPAE/SEVAC/DeleteCategory/<int:pk>",views.sevac_delete_category,name="SevacDeleteCategory"),
    #path("SMAPAE/SEVAC/SelectCategoriesSevac",views.select_categories_sevac,name="select_categories_sevac"),
    path("SMAPAE/SEVAC/ListSubcategories",views.sevac_list_subcategories,name="SevacListSubcategories"),
    path("SMAPAE/SEVAC/NewSubcategories/<int:year>/<int:category>/",views.sevac_new_subcategory,name="SevacNewSubcategory"),
    path("SMAPAE/SEVAC/SaveSubcategory",views.sevac_save_subcategory,name="SevacSaveSubcategory"),
    path("SMAPAE/SEVAC/DetailSubcategory/<int:year>/<int:subcategory>/",views.sevac_detail_subcategory,name="SevacDetailSubcategory"),
    path('SMAPAE/SEVAC/ListarDocumentos/year/<int:year>/subcategory/<int:subcategory>', views.ListarDocumentosSevac, name='ListarDocumentosSevac'),
    path("SMAPAE/SEVAC/NewDocument",views.SevacNewDocument,name="SevacNewDocument"),
    path("SMAPAE/SEVAC/EditSubcategories/<int:pk>",views.sevac_edit_subcategory,name="SevacEditSubcategory"),
    path("SMAPAE/SEVAC/DeleteSubcategories/<int:pk>",views.sevac_delete_subcategory,name="SevacDeleteSubcategory"),

    #path("SMAPAE/SEVAC/ListDocuments",views.sevac_list_documents,name="SevacListDocuments"),
    #path("SMAPAE/SEVAC/NewDocument",views.sevac_new_document,name="SevacNewdocument"),
    #path("SMAPAE/SEVAC/EditDocument",views.sevac_edit_document,name="SevacEditdocument"),
    path("SMAPAE/SEVAC/DeleteDocument/<int:pk>",views.sevac_delete_document,name="SevacDeleteDocument"),    
    # ?COTAIPEC-transparencia
    path("transparency/COTAIPEC", views.cotaipec_view, name="cotaipec_view"),
    path("transparency/COTAIPEC/new",views.cotaipec_document_new,name="cotaipec_document_new"),
    path("transparency/COTAIPEC/delete/<int:pk>/",views.cotaipec_document_delete,name="cotaipec_document_delete"),
    path("transparency/COTAIPEC/list",views.cotaipec_document_list,name="cotaipec_document_list"),
    path("transparency/COTAIPEC/menu",views.menu_cotaipec_view.as_view(),name="menu_cotaipec"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
