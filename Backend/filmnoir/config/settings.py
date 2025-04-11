import sys
import os
from pathlib import Path
from typing import Mapping, Any
from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.parent / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = '/media/'

DEBUG = True

ALLOWED_HOSTS: list[str] = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",

    "domain",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

###################################################################################################
MODE: str | None = os.getenv("MODE")
if MODE is None:
    raise RuntimeError("MODE environment variable is not set.")

########################
# LOGURU CONFIGURATION #
########################
LOGURU_LOG_LEVEL: str | None = os.getenv("LOGURU_LOG_LEVEL")

if LOGURU_LOG_LEVEL is None:
    raise RuntimeError("LOGURU_LOG_LEVEL env var is not set")


def format_record(record: Mapping[str, Any]) -> str:
    record["extra"]["rel_path"] = Path(record["file"].path).relative_to(BASE_DIR)

    msg = record["message"]
    result = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{extra[rel_path]}</cyan>[<cyan>{line}</cyan>] (<cyan>{function}</cyan>) ----> "
    )
    if "=" in msg:
        parts = msg.split("=", 1)
        record["extra"]["left"] = parts[0].strip()
        record["extra"]["right"] = parts[1].strip()
        result = result + "<level>{extra[left]}  =  {extra[right]}</level>\n"
    else:
        result = result + "<level>{message}</level>\n"
    return result


logger.remove()

logger.add(
    sys.stdout,
    format=format_record,
    level=LOGURU_LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
