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
    path("Accounting/NewCategory",views.AccountingNewCategory,name="AccountingNewCategory"),
    path("Accounting/NewSubcategory",views.AccountingNewSubcategory,name="AccountingNewSubcategory",),
    path("Accounting/NewDocument",views.AccountingNewDocument,name="AccountingNewDocument"),
    path("Accounting/ListCategories",views.AccountingListCategories,name="AccountingListCategories"),
    path("Accounting/ListSubcategories",views.AccountingListSubcategories,name="AccountingListSubcategories"),
    path("AccountingListDocuments",views.AccountingListDocuments,name="AccountingListDocuments"),
    path("Accounting/EditCategory/<int:pk>/",views.AccountingEditCategory,name="AccountingEditCategory"),
    path("Accounting/EditSubcategory/<int:pk>/",views.AccountingEditSubcategory,name="AccountingEditSubcategory"),
    path("Accounting/EditDocument/<int:pk>/",views.AccountingEditDocument,name="AccountingEditDocument"),
    path("Accounting/DetailCategory/<int:pk>/",views.AccountingDetailCategory,name="AccountingDetailCategory"),
    path("Accounting/DetailSubcategory/<int:pk>/",views.AccountingDetailSubcategory,name="AccountingDetailSubcategory"),
    path("Accounting/SelectCategories",views.AccountingSelectCategories,name="AccountingSelectCategories"),
    path("Accounting/SelectCategoriesInDocuments",views.AccountingSelectCategoriesInDocuments,name="AccountingSelectCategoriesInDocuments"),
    path("Accounting/SelectSubcategories",views.AccountingSelectSubcategories,name="AccountingSelectSubcategories"),
    path("Accounting/DeleteDocument/<int:pk>/",views.AccountingDeleteDocument,name="AccountingDeleteDocument"),
    path("Accounting/ListYearsInDocuments",views.AccountingListYearsInDocuments,name="AccountingListYearsInDocuments")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
