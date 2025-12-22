import os
from pathlib import Path
from dotenv import load_dotenv

# === 讀取環境變數 ===
load_dotenv()

# === 基本路徑設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === 安全設定 ===
SECRET_KEY = os.getenv("SECRET_KEY", "your-dev-secret-key")
DEBUG = True
ALLOWED_HOSTS = []

# ============================================================
# 🚀 已安裝的 App
# ============================================================
INSTALLED_APPS = [
    # Django 內建
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",   # ⭐ 必須

    # ⭐ allauth（SSO 核心）
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # 🌈 Planora 模組
    "apps.core",
    "apps.personal",
    "apps.accounts",
    "apps.treedoc",

    # ⭐ Celery Beat
    "django_celery_beat",
]


# ============================================================
# 🧱 Middleware
# ============================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

# ============================================================
# 🌐 URL
# ============================================================
ROOT_URLCONF = "config.urls"

# ============================================================
# 🖼 Templates
# ============================================================
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
            ],
        },
    },
]

# ============================================================
# ⚙ WSGI
# ============================================================
WSGI_APPLICATION = "config.wsgi.application"

# ============================================================
# 🗄 Database
# ============================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ============================================================
# 🔐 Password validation
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# ============================================================
# 🌍 i18n / timezone
# ============================================================
LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
USE_I18N = True
USE_TZ = True
SITE_ID = 1
# ============================================================
# 📦 Static / Media
# ============================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "uploads"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# 🔐 Login / Logout
# ============================================================
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
LOGIN_URL = "accounts:login"

# ============================================================
# 🧠 Redis Cache（功能 ①）
# ============================================================
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv(
            "REDIS_URL",
            "redis://127.0.0.1:6379/1"
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ============================================================
# ⚙ Celery（功能 ③）
# ============================================================
CELERY_BROKER_URL = os.getenv(
    "REDIS_URL",
    "redis://127.0.0.1:6379/2"
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Taipei"

# ============================================================
# ⏰ Celery Beat（功能 ④）
# ============================================================
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


# ============================================================
# ✉️ Email（開發 / Demo 階段：不真的寄信）
# ============================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# allauth：關閉 email 驗證（專題 / demo 用）
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_REQUIRED = False




# 刪除最後面那兩段重複的 SOCIALACCOUNT_PROVIDERS，改用這段：
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            # 優先讀取環境變數，讀不到再用你提供的硬編碼值（方便佈署）
            'client_id': os.getenv('GOOGLE_CLIENT_ID', '1058221232607-humrhvv8c6kvltnj456qk71u54m2qoc9.apps.googleusercontent.com'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET', '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'),
            'key': ''
        },
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}