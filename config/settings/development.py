"""
開發環境設定：Planora development settings
"""
from .base import *
import os

# ============================================================
# 基本開發設定
# ============================================================

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ============================================================
# Database（SQLite，開發用）
# ============================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ============================================================
# Email（開發環境：印在 console）
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ============================================================
# Google OAuth（開發）
# ============================================================

SOCIALACCOUNT_PROVIDERS["google"]["APP"] = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "key": "",
}

# ============================================================
# Security（開發模式不強制 HTTPS）
# ============================================================

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# ============================================================
# ❗❗ 不要在 development.py 再設定 Redis / Celery
# ❗❗ 全部吃 base.py（這樣才能部署）
# ============================================================


