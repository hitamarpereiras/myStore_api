from pathlib import Path
from config import thi_settings
import dj_database_url
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!myuvwl4g*rp8ugg9^u$k=ow$!a(ro-78exi+-oihv8xy^cyqm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "mystore-api-n1f9.onrender.com",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://mystore-api-n1f9.onrender.com",
    "http://localhost:3000",     # se tiver frontend local
    "http://127.0.0.1:3000",
]

CORS_ALLOWED_ORIGINS = [
    "https://mystore-api-n1f9.onrender.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True


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
    'apps.stores',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
        conn_max_age=200,
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
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

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

    "site_icon": "img/logo.jpg",

    "site_logo": "img/logo.jpg",

    "login_logo": "img/logo.jpg",

    # Copyright on the footer
    "copyright": "Hitamar Silva®",

    # Menu
     "topmenu_links": [
        {"app": "stores"},
        {"name": "Suporte", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

     ],

    # Construtor de interface
    "show_ui_builder": True,
}