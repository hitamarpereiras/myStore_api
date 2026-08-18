import os
from pathlib import Path
from config import thi_settings
import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from datetime import timedelta
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
_django_secret_key = os.environ.get("DJANGO_SECRET_KEY")
if os.environ.get("VERCEL") and not _django_secret_key:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY must be configured in Vercel.")

SECRET_KEY = _django_secret_key or "django-insecure-local-development-key-change-before-production"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = thi_settings.DEBUG

ALLOWED_HOSTS = [
    "mystore-api-n1f9.onrender.com",
    "adm-loja.vercel.app",
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]

ALLOWED_HOSTS += [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    "https://mystore-api-n1f9.onrender.com",
    "https://adm-loja.vercel.app",
    "http://localhost:5500",     # se tiver frontend local
    "http://127.0.0.1:5500",
]

CORS_ALLOWED_ORIGINS = [
    "https://mystore-api-n1f9.onrender.com",
    "https://adm-loja.vercel.app",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

CORS_ALLOWED_ORIGINS += [
    origin.strip()
    for origin in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]

CORS_ALLOW_HEADERS = [
    *default_headers,
    "x-store-id",
]

CORS_ALLOW_CREDENTIALS = True

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = 31536000
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework',
    'django_filters',

    'apps.authentication',
    'apps.accounts',
    'apps.categories',
    'apps.stores',
    'apps.products',
    'apps.orders',
    'apps.sales',
    'apps.customers',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse(
        thi_settings.DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}

DATABASES['default']['OPTIONS'] = {
    'sslmode': 'require'
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = (
    "whitenoise.storage.CompressedManifestStaticFilesStorage"
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 1000000 # 1MB


AUTH_USER_MODEL = 'accounts.User'


# Django REST Framework settings

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    'DEFAULT_PAGINATION_CLASS': 'core.pagination.DefaultPagination',
    'PAGE_SIZE': 40,

}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),  # tempo do token de acesso
    'REFRESH_TOKEN_LIFETIME': timedelta(days=20),     # tempo do refresh
    'ROTATE_REFRESH_TOKENS': True, # Gera um novo  refresh token a cada refresh 
    'BLACKLIST_AFTER_ROTATION': True, # Invalida o refresh token antigo após a rotação
}


# interface django admin

JAZZMIN_SETTINGS = {
    "site_title": "My Store API",

    "site_icon": "img/favicon.png",

    "site_logo": "img/logo2.png",

    "login_logo": "img/logo2.png",

    # Copyright on the footer
    "copyright": "Hitamar Silva®",

    # Menu
     "topmenu_links": [
        {"app": "stores"},
        {"name": "Suporte", "url": "https://github.com/hitamarpereiras", "new_window": True},

     ],

    # Construtor de interface
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": True,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "united",
    "default_theme_mode": "dark",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}
