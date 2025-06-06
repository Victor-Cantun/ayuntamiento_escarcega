"""escarcega URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
#from apps.a_home.views import *
from apps.a_users.views import profile_view
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
#from .views import index

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    #path("", home_view, name="home"),
    path("",include("apps.a_home.urls")),
    path("", include("apps.core.urls")),
    path("", include("apps.a_income.urls")),
    path("", include("apps.a_payroll.urls")),
    path("", include("apps.website.urls")),
    path("police/",include("apps.a_police.urls")),
    path("profile/", include("apps.a_users.urls")),
    path("", include("apps.a_chat.urls")),
    path("@<username>/", profile_view, name="profile"),
    path("", include("apps.a_notifications.urls")),
    path("select2/", include("django_select2.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
