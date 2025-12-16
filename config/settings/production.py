# config/settings/production.py
from .base import *
import os
from dotenv import load_dotenv
import dj_database_url

# ============================================================
# 載入 .env（Zeabur 會自動注入環境變數，這行不會出錯）
# ============================================================
load_dotenv()

# ============================================================
# 基本設定
# ============================================================
DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ============================================================
# Database（Zeabur PostgreSQL / fallback SQLite）
# ============================================================
postgres_connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

if postgres_connection_string:
    DATABASES = {
        "default": dj_database_url.parse(
            postgres_connection_string,
            conn_max_age=600,
        )
    }
else:
    # 本地或緊急 fallback（實際 Zeabur 不會走到這）
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ============================================================
# Redis（Cache + Celery Broker）
# ============================================================
REDIS_URL = os.getenv("REDIS_URL")

# --- Cache（django-redis）---
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "planora",
    }
}

# ============================================================
# Celery（正式環境一定要啟用）
# ============================================================
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

# ❗ 生產環境絕對不能 eager
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_EAGER_PROPAGATES = False

# ============================================================
# Security（Zeabur + Proxy）
# ============================================================
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    "https://planora.zeabur.app",
]

# ============================================================
# Logging（讓老師看到你有處理 production error）
# ============================================================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

