import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
dotenv_path = BASE_DIR / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# -----------------------------
# Security Settings
# -----------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-change-this')
DEBUG = os.environ.get('DEBUG', '0') == '1'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')

# -----------------------------
# Application Definition
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'django_htmx',
    'simple_history',
    'smart_selects',
    'drf_spectacular',
    
    # Project apps
    'authentication',
    'vendors',
    'products',
    'assets',
    'dashboard',
    'recycle_bin',
    'upload',
    'error_handlers',
    'roles',
    'users',
    'support',
    'notifications',
    'configurations',
    'audit',
    'license',
]

# -----------------------------
# Middleware Configuration
# -----------------------------
MIDDLEWARE = [
    # Authentication middleware should be FIRST if it checks database connections
    # But let's move it AFTER security for better compatibility
    'django.middleware.security.SecurityMiddleware',
    
    # WhiteNoise MUST come right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Simple History middleware
    'simple_history.middleware.HistoryRequestMiddleware',
    
    # HTMX middleware
    'django_htmx.middleware.HtmxMiddleware',
    
    # Custom middleware at the END to avoid URL resolution issues
    'authentication.middleware.DBConnectionMiddleware',
]

# -----------------------------
# URL Configuration
# -----------------------------
ROOT_URLCONF = 'AssetManagement.urls'
WSGI_APPLICATION = 'AssetManagement.wsgi.application'

# -----------------------------
# Database Configuration
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.postgresql'),
        'NAME': os.environ.get('DATABASE_NAME', 'asseto_db'),
        'USER': os.environ.get('DATABASE_USER', 'asseto_user'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'asseto_pass_123'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
    }
}

# -----------------------------
# Templates Configuration
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'configurations.context_processors.sidebar_logo',
                'configurations.context_processors.favicon_image',
                'configurations.context_processors.login_page_logo'
            ],
        },
    },
]

# -----------------------------
# Password Validation
# -----------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------
# Static Files Configuration
# -----------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# WhiteNoise configuration for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# -----------------------------
# Custom User Model
# -----------------------------
AUTH_USER_MODEL = 'authentication.User'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -----------------------------
# Login/Logout URLs
# -----------------------------
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = 'authentication:login'

# -----------------------------
# Email Configuration
# -----------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# -----------------------------
# Django Resized Settings
# -----------------------------
DJANGORESIZED_DEFAULT_SIZE = [1024, 768]
DJANGORESIZED_DEFAULT_QUALITY = 75
DJANGORESIZED_DEFAULT_KEEP_META = True
DJANGORESIZED_DEFAULT_FORCE_FORMAT = 'JPEG'
DJANGORESIZED_DEFAULT_FORMAT_EXTENSIONS = {'JPEG': ".jpg"}
DJANGORESIZED_DEFAULT_NORMALIZE_ROTATION = True

DATA_UPLOAD_MAX_NUMBER_FIELDS = 3000
APPEND_SLASH = True

# -----------------------------
# REST Framework Configuration
# -----------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# -----------------------------
# Simple JWT Configuration
# -----------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=720) if not DEBUG else timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

# -----------------------------
# DRF Spectacular Configuration
# -----------------------------
SPECTACULAR_SETTINGS = {
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_OPTIONS': {'persistAuthorization': True},
}

# -----------------------------
# Logging Configuration (Production)
# -----------------------------
if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {message}',
                'style': '{',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
