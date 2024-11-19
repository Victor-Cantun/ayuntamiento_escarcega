from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # ListarCabildo
    path("listCouncil", views.listCouncil, name="listCouncil"),
    # ListarSlider
    path("listCarousel", views.listCarousel, name="listCarousel"),
    # ListarDependencias
    path("listDependences", views.listDependences, name="listDependences"),
    # ListarContabiliidad
    path("listAccounting", views.listAccounting, name="listAccounting"),
    # ListarBlog
    path("listPosts", views.listPosts, name="listPosts"),
    # *?VIEWS
    path("", views.start, name="start"),
    # path('register',views.register_user, name='register'),
    path("login", views.login_user, name="login"),
    path("logout", views.exit, name="logout"),
    path("home", views.home, name="home"),
    path("list_council", views.list_council, name="list_council"),
    path("newCouncil", views.newCouncil, name="newCouncil"),
    path("editCouncil", views.editCouncil, name="editCouncil"),
    path("editCouncil/<int:pk>", views.editCouncil, name="editCouncil"),
    path("deleteCouncil/<int:pk>", views.deleteCouncil, name="deleteCouncil"),
    path("list_directors", views.list_directors, name="list_directors"),
    path("newDirector", views.newDirector, name="newDirector"),
    path("editDirector", views.editDirector, name="editDirector"),
    path("editDirector/<int:pk>", views.editDirector, name="editDirector"),
    path("deleteDirector/<int:pk>", views.deleteDirector, name="deleteDirector"),
    path("list_dependences", views.list_dependences, name="list_dependences"),
    path("newDependence", views.newDependence, name="newDependence"),
    path("editDependence", views.editDependence, name="editDependence"),
    path("editDependence/<int:pk>", views.editDependence, name="editDependence"),
    path("deleteDependence/<int:pk>", views.deleteDependence, name="deleteDependence"),
    path("list_carousel", views.list_carousel, name="list_carousel"),
    path("newCarousel", views.newCarousel, name="newCarousel"),
    path("editCarousel", views.editCarousel, name="editCarousel"),
    path("editCarousel/<int:pk>", views.editCarousel, name="editCarousel"),
    path("deleteCarousel/<int:pk>", views.deleteCarousel, name="deleteCarousel"),
    path("list_accounting", views.list_accounting, name="list_accounting"),
    path("newAccounting", views.newAccounting, name="newAccounting"),
    path("editAccounting", views.editAccounting, name="editAccounting"),
    path("editAccounting/<int:pk>", views.editAccounting, name="editAccounting"),
    path("deleteAccounting/<int:pk>", views.deleteAccounting, name="deleteAccounting"),
    path("list_gazette", views.list_gazette, name="list_gazette"),
    path("newGazette", views.newGazette, name="newGazette"),
    path("editGazette", views.editGazette, name="editGazette"),
    path("editGazette/<int:pk>", views.editGazette, name="editGazette"),
    path("deleteGazette/<int:pk>", views.deleteGazette, name="deleteGazette"),
    path("list_document", views.list_document, name="list_document"),
    path("newDocument", views.newDocument, name="newDocument"),
    path("editDocument", views.editDocument, name="editDocument"),
    path("editDocument/<int:pk>", views.editDocument, name="editDocument"),
    path("deleteDocument/<int:pk>", views.deleteDocument, name="deleteDocument"),
    path("list_posts", views.list_posts, name="list_posts"),
    path("newPost", views.newPost, name="newPost"),
    path("editPost", views.editPost, name="editPost"),
    path("editPost/<int:pk>", views.editPost, name="editPost"),
    path("deletePost/<int:pk>", views.deletePost, name="deletePost"),
    # *?CRUD
    path("createPost/", views.CreatePostView.as_view(), name="createPost"),
    path("carousel/", views.carouselListCreateView.as_view(), name="carousel-lc"),
    path(
        "carousel/<int:pk>/",
        views.carouselUpdateDestroyView.as_view(),
        name="carousel-rud",
    ),
    path("accounting/", views.accountingListCreateView.as_view(), name="accounting-lc"),
    path("user", views.UserDetail.as_view(), name="user_detail"),
    path("positions/", views.PositionsListCreateView.as_view(), name="positions-lc"),
    path("council/", views.CouncilListCreateView.as_view(), name="council-lc"),
    path(
        "council/<int:pk>/",
        views.CouncilUpdateDestroyView.as_view(),
        name="council-rud",
    ),
    path("directors/", views.DirectorsListCreateView.as_view(), name="directors-lc"),
    path(
        "directors/<int:pk>/",
        views.DirectorsUpdateDestroyView.as_view(),
        name="directors-rud",
    ),
    path(
        "dependences/", views.DependencesListCreateView.as_view(), name="dependences-lc"
    ),
    path(
        "dependences/<int:pk>/",
        views.DependencesUpdateDestroyView.as_view(),
        name="dependences-rud",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
