from pathlib import Path
import json

with open("/etc/wagone_be_config.json") as config_file:
    config = json.load(config_file)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config["SECRET_KEY"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "accounts",
    "chat",
    "core",
    "corsheaders",
    "phonenumber_field",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "wagone_be.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "wagone_be.wsgi.application"
ASGI_APPLICATION = "wagone_be.asgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

FRONTEND_BASE_URL = config.get("FRONTEND_BASE_URL")
FRONTEND_PASSWORD_RESET_PATH = config.get("FRONTEND_PASSWORD_RESET_PATH")
FRONTEND_ACCOUNT_VERIFICATION_PATH = config.get(
    "FRONTEND_ACCOUNT_VERIFICATION_PATH"
)

DJANGO_SU_NAME = config.get("DJANGO_SU_NAME")
DJANGO_SU_EMAIL = config.get("DJANGO_SU_EMAIL")
DJANGO_SU_PASSWORD = config.get("DJANGO_SU_PASSWORD")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "core.utils.custom_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"}
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {"format": "{levelname} {message}", "style": "{"},
    },
    "root": {"handlers": ["console"], "level": "INFO"},
}


PHONENUMBER_DEFAULT_REGION = "NG"
PHONENUMBER_DB_FORMAT = "INTERNATIONAL"
PHONENUMBER_REGEX_PATTERN = "((^\+234)(\d{10}))|((^070)([0-9]))(\d{7})|((^090)([0-9]))(\d{7})|((^091)([0-9]))(\d{7})|((^071)([0-9]))(\d{7})|((^080)([0-9]))(\d{7})|((^081)([0-9]))(\d{7})"  # noqa

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "TIMEOUT": 600,
        "LOCATION": config.get("CELERY_BROKER_URL"),
        "KEY_PREFIX": "wagone_be",
    }
}

BROKER_URL = config.get("CELERY_BROKER_URL")
CELERY_BROKER_URL = config.get("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config.get("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
