from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("ayuntamiento", views.cityHall, name="cityHall"),
    path("listDirectors", views.listDirectors, name="listDirectors"),
    path("listDependences", views.listDependences, name="listDependences"),
    path("listDepartments", views.listDepartments, name="listDepartments"),
    path("editDirector/<int:pk>", views.editDirector, name="editDirector"),
    path("editDependence/<int:pk>", views.editDependence, name="editDependence"),
    path("editDepartment/<int:pk>", views.editDepartment, name="editDepartment"),
    path("newDirector", views.newDirector, name="newDirector"),
    path("newDependence", views.newDependence, name="newDependence"),
    path("newDepartment", views.newDepartment, name="newDepartment"),
    path("detailDirector/<int:pk>", views.detailDirector, name="detailDirector"),
    path("detailDependence/<int:pk>", views.detailDependence, name="detailDependence"),
    path("detailDepartment/<int:pk>", views.detailDepartment, name="detailDepartment"),
    # GESTIONES
    path("procedures", views.procedures, name="procedures"),
    path(
        "listRequestProcedures",
        views.listRequetsProcedures,
        name="listRequestProcedures",
    ),
    path(
        "detailRequestProcedure/<int:pk>",
        views.detailRequestProcedure,
        name="detailRequestProcedure",
    ),
    path("newRequestProcedure", views.newRequestProcedure, name="newRequestProcedure"),
    path(
        "editRequestProcedure/<int:pk>",
        views.editRequestProcedure,
        name="editRequestProcedure",
    ),
    path(
        "deleteRequestProcedure/<int:pk>",
        views.deleteRequestProcedure,
        name="deleteRequestProcedure",
    ),
    path("searchCitizen", views.searchCitizen, name="searchCitizen"),
    path("newCitizen", views.newCitizen, name="newCitizen"),
    path("editCitizen/<int:pk>", views.editCitizen, name="editCitizen"),
    path(
        "newTrackingProcedure/<int:pk>",
        views.newTrackingProcedure,
        name="newTrackingProcedure",
    ),
    path(
        "saveTrackingProcedure",
        views.saveTrackingProcedure,
        name="saveTrackingProcedure",
    ),
    path("showProcedure/<int:pk>", views.showProcedure, name="showProcedure"),
    path("uploadEvidence/<int:pk>", views.uploadEvidence, name="uploadEvidence"),
    path(
        "addCommentProcedure/<int:pk>",
        views.addCommentProcedure,
        name="addCommentProcedure",
    ),
    path(
        "addDocumentProcedure/<int:pk>",
        views.addDocumentProcedure,
        name="addDocumentProcedure",
    ),
    path(
        "addEvidenceProcedure/<int:pk>",
        views.addEvidenceProcedure,
        name="addEvidenceProcedure",
    ),
    path(
        "addDeliveryProcedure/<int:pk>",
        views.addDeliveryProcedure,
        name="addDeliveryProcedure",
    ),
    path(
        "editStatusRequestProcedure/<int:pk>",
        views.editStatusRequestProcedure,
        name="editStatusRequestProcedure",
    ),
    path(
        "shareRequestProcedure/<int:pk>",
        views.shareRequestProcedure,
        name="shareRequestProcedure",
    ),
    path("typesDocument", views.typesDocument, name="typesDocument"),
    path("newTypeDocument", views.newTypeDocument, name="newTypeDocument"),
    path("newTypeProcedure", views.newTypeProcedure, name="newTypeProcedure"),
    path("typesProcedure", views.typesProcedure, name="typesProcedure"),
    path(
        "saveAccountingMoment/<int:pk>",
        views.saveAccountingMoment,
        name="saveAccountingMoment",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
