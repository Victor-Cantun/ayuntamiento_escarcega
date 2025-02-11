"""
Django settings for escarcega project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# para mostra imagenes
import os

# para usar mensajes
from django.contrib.messages import constants as messages

# para manejar el tiempo en restframeworkjwt
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7odi=n25g&9myf&c(x!a&f$ogl7yrf2ly5^8)bj%m*pu7vqa2="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4321",
]
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ["localhost", "153.92.214.26", "*", "localhost:4321"]

# Application definition

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "django_cleanup.apps.CleanupConfig",
    "allauth",
    "allauth.account",
    "django_htmx",
    "core",
    "a_home",
    "a_users",
    "a_chat",
    "a_notifications",
    "website",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]


AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "a_users.auth_backend.CustomAuthBackend",
]


MESSAGE_TAGS = {
    messages.DEBUG: "alert-dark",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

ROOT_URLCONF = "escarcega.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI_APPLICATION = "escarcega.wsgi.application"
ASGI_APPLICATION = "escarcega.asgi.application"
#CACHES = {
#    "default": {
#        "BACKEND": "django_redis.cache.RedisCache",
#        "LOCATION": "redis://localhost:6379/1",  # Cambia 'localhost' por la IP si Redis está en otro servidor
#        "OPTIONS": {
#            "CLIENT_CLASS": "django_redis.client.DefaultClient",
#        }
#    }
#}
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
        #"BACKEND": "channels_redis.core.RedisChannelLayer",
        #"CONFIG": {
        #        "hosts": [("localhost", 6379)],  # Cambia 'localhost' si es remoto
        #},
    }

}

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "NAME": "ayuntamiento_esc",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "postgres",
        "PASSWORD": "vicodev24$",
        "HOST": "localhost",
        "PORT": "5433",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "es-mx"

TIME_ZONE = "America/Merida"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

COMPRESS_ROOT = BASE_DIR / "static"

COMPRESS_ENABLED = True

STATICFILES_FINDERS = ("compressor.finders.CompressorFinder",)

#COMPRESS_EXCLUDE = ["static/admin/css/", "static/admin/js/", "static/admin/img/"]
#STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "static/"
#STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "media/"
#MEDIA_ROOT = [BASE_DIR, "media"]
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# LOGOUT_URL = "login"
# LOGIN_URL = "login"



REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
}

# Configuración del backend de correo
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"  # Servidor SMTP de Gmail
EMAIL_PORT = 587  # Puerto para TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "cantundominguez@gmail.com"  # Tu dirección de correo de Gmail
EMAIL_HOST_PASSWORD = "mcithddzfuyxdmow"  # La contraseña de tu correo

# Configuración de correo predeterminada
DEFAULT_FROM_EMAIL = "cantundominguez@gmail.com"

LOGIN_REDIRECT_URL = "/"
ACCOUNT_SIGNUP_REDIRECT_URL = "{% url 'account_signup' %}?next={% url 'profile-onboarding' %}"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True 
ACCOUNT_USERNAME_REQUIRED = False
#ACCOUNT_EMAIL_VERIFICATION = "optional"

# Login personalizado
#ACCOUNT_FORMS = {"login": "a_users.forms.CustomLoginForm"}
