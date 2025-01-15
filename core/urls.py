from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ListarCabildo
    path("procedures", views.procedures, name="procedures"),
    path("listRequestProcedures",views.listRequetsProcedures,name="listRequestProcedures"),
    path("detailRequestProcedure/<int:pk>",views.detailRequestProcedure,name="detailRequestProcedure"),
    path("newRequestProcedure",views.newRequestProcedure,name="newRequestProcedure"),
    path("editRequestProcedure/<int:pk>", views.editRequestProcedure, name="editRequestProcedure"),
    path("deleteRequestProcedure/<int:pk>", views.deleteRequestProcedure, name="deleteRequestProcedure"),
    path("searchCitizen",views.searchCitizen,name="searchCitizen"),
    path("newCitizen",views.newCitizen,name="newCitizen"),
    path("newTrackingProcedure/<int:pk>",views.newTrackingProcedure,name="newTrackingProcedure"),
    path("saveTrackingProcedure",views.saveTrackingProcedure,name="saveTrackingProcedure"),
    
    path("showProcedure/<int:pk>",views.showProcedure,name="showProcedure"),
    path("uploadEvidence/<int:pk>",views.uploadEvidence,name="uploadEvidence"),
    #path("saveEvidenceProcedure",views.saveEvidenceProcedure,name="saveEvidenceProcedure"),

    path("addCommentProcedure",views.addCommentProcedure,name="addCommentProcedure"),
    path("addDocumentProcedure",views.addDocumentProcedure,name="addDocumentProcedure"),
    path("addEvidenceProcedure",views.addEvidenceProcedure,name="addEvidenceProcedure"),
    path("addDeliveryProcedure",views.addDeliveryProcedure,name="addDeliveryProcedure"),
    path("editStatusRequestProcedure/<int:pk>", views.editStatusRequestProcedure, name="editStatusRequestProcedure"),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
