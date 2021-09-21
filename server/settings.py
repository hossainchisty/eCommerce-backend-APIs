"""
Title: eCommerce back-end API
Description: An e-commerce platform.
Author: Hossain Chisty(Backend Developer)
Contact: hossain.chisty11@gmail.com
Github: https://github.com/hossainchisty

"""

from pathlib import Path
from decouple import config
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "5cf^a+ytg^4g(hv=m#x1_p-^mlq&(&0f8(6jbdp0h4g^z07z*v"

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "taggit",
    "corsheaders",
    "rest_framework",
    "django_countries",
    "django.contrib.sites",
    "rest_framework_swagger",
    "django.contrib.sitemaps",
    # local
    "api.apps.ApiConfig",
]

SITE_ID = 1


# django-cors-headers is a Django application for handling the server headers required for Cross-Origin Resource Sharing (CORS).
# CORS_ALLOWED_ORIGINS = [
#     "https://example.com",
#     "https://sub.example.com",
#     "http://localhost:8080",
#     "http://127.0.0.1:9000"
# ]

# CORS_ORIGIN_WHITELIST = (
#     'localhost:3000', # react
# )

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "server.urls"

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

WSGI_APPLICATION = "server.wsgi.application"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


# REST-API Permissions
REST_FRAMEWORK = {
    # IsAuthenticated
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # "DEFAULT_AUTHENTICATION_CLASSES": (
    #     "rest_framework_simplejwt.authentication.JWTAuthentication",
    # ),
    # For Production Only
    # "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

REST_FRAMEWORK = {"DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema"}


"""
To enable the PageNumberPagination style globally
"""
# REST-API Pagination
# REST_FRAMEWORK = {
#     "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
#     "PAGE_SIZE": 2,
# }

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"


MEDIA_ROOT = BASE_DIR / "static/images"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Custom user model
AUTH_USER_MODEL = "api.CustomUser"


# SMTP Configuration
# EMAIL_HOST = "smtp.zoho.com"
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "hossain.chisty@zohomail.com"
# EMAIL_HOST_PASSWORD = "#2#3B399TiU@aBC"
# EMAIL_USE_SSL = True
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
