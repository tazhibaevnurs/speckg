from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name: str, default: str = "") -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env_bool("DJANGO_DEBUG", True)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "http://localhost:8000,http://127.0.0.1:8000",
)

# Render / Railway / Koyeb inject the public hostname
for _host_key in ("RENDER_EXTERNAL_HOSTNAME", "RAILWAY_PUBLIC_DOMAIN"):
    _host = os.getenv(_host_key, "").strip()
    if not _host:
        continue
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)
    _origin = f"https://{_host}"
    if _origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_origin)

if os.getenv("RENDER"):
    if ".onrender.com" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(".onrender.com")

SITE_URL = os.getenv("SITE_URL", "http://127.0.0.1:8000").rstrip("/")
_public_host = os.getenv("RENDER_EXTERNAL_HOSTNAME") or os.getenv("RAILWAY_PUBLIC_DOMAIN")
if _public_host and SITE_URL.startswith("http://127"):
    SITE_URL = f"https://{_public_host}".rstrip("/")
SITE_NAME = "SPEC-KG"

# Contacts — placeholders, swap via .env without touching templates
CONTACT_PHONE = os.getenv("CONTACT_PHONE", "+996 506 055 056")
CONTACT_PHONE_TEL = os.getenv("CONTACT_PHONE_TEL", "+996506055056")
CONTACT_WHATSAPP = os.getenv("CONTACT_WHATSAPP", "+996506055056")
CONTACT_TELEGRAM = os.getenv("CONTACT_TELEGRAM", "@tazhibaevn")
CONTACT_TELEGRAM_URL = os.getenv("CONTACT_TELEGRAM_URL", "https://t.me/tazhibaevn")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "info@spec-kg.com")
CONTACT_CITY = os.getenv("CONTACT_CITY", "Бишкек, Кыргызстан")

WHATSAPP_URL = f"https://wa.me/{CONTACT_WHATSAPP.lstrip('+').replace(' ', '')}"

# Calculator: stub FX rate, not a live market feed
EXCHANGE_USD_RUB = float(os.getenv("EXCHANGE_USD_RUB", "90"))

# Rounded reference magnitudes of RF commercial recycling fee (not a legal calc)
UTIL_FEE_RUB = {
    "tractor": int(os.getenv("UTIL_FEE_TRACTOR", "3500000")),
    "dump": int(os.getenv("UTIL_FEE_DUMP", "2800000")),
    "chassis": int(os.getenv("UTIL_FEE_CHASSIS", "2200000")),
    "other": int(os.getenv("UTIL_FEE_OTHER", "1500000")),
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "").strip()

LEGAL_DISCLAIMER = (
    "SPEC-KG не оказывает юридическую консультацию. Условия оформления, налоги "
    "и правила эксплуатации зависят от статуса клиента и актуального законодательства "
    "РФ, КР и ЕАЭС и могут меняться. Итоговая схема согласуется индивидуально. "
    "Сайт носит информационный характер."
)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    "pages.apps.PagesConfig",
    "catalog.apps.CatalogConfig",
    "leads.apps.LeadsConfig",
    "calculator.apps.CalculatorConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middleware.SecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"

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
                "pages.context_processors.site_context",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage"
            if DEBUG
            else "whitenoise.storage.CompressedStaticFilesStorage"
        )
    },
}

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Staff-only for now; default User is enough for a future cabinet
LOGIN_URL = "/admin/login/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "[{levelname}] {name}: {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "loggers": {
        "leads": {"handlers": ["console"], "level": "INFO"},
        "django.request": {"handlers": ["console"], "level": "WARNING"},
    },
}

# HTTPS / cookie hardening — active when DEBUG is off (VPS / production)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.getenv("SECURE_HSTS_SECONDS", "31536000"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = False
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
