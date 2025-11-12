"""
開發環境設定：Planora development settings
"""
from .base import *
import os

# === 開發模式 ===
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# === 本地資料庫設定 ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === 信件設定（開發階段印在 Console） ===
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# === Google OAuth 回調網址 ===
# ⚠️ 一定要在 Google Cloud Console 的 OAuth 同意畫面與 Authorized redirect URI 設以下兩個：
# http://127.0.0.1:8000/accounts/google/login/callback/
# http://localhost:8000/accounts/google/login/callback/

SOCIALACCOUNT_PROVIDERS['google']['APP'] = {
    'client_id': os.getenv('GOOGLE_CLIENT_ID'),
    'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
    'key': ''
}

# === 開發環境的安全性設定（方便除錯，不開啟強制 HTTPS） ===
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

