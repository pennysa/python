from .base import *

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ⚠️ 重點：development.py **絕對不要** 出現
# SOCIALACCOUNT_PROVIDERS["google"]["APP"]



