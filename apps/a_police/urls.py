from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet, basename='documents')

urlpatterns = [
    path('auth/register/', views.UserRegistrationView.as_view(), name='register'),
    path('auth/login/', views.UserLoginView.as_view(), name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/profile/', views.user_profile_view, name='user_profile'),
    path('upload/', views.UploadPDFView.as_view(), name='upload-pdf'),
    # URLs de documentos
    path('', include(router.urls)),
# TODO: PENEL ADMINISTRATIVO   
    path("police", views.police_admin, name="police_admin"),
    path("police_applicants_list", views.police_applicants_list, name="police_applicants_list"),
    path("police_applicant_detail/<int:pk>",views.police_applicant_detail, name="police_applicant_detail"),    
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)