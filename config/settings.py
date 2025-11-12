import os
from pathlib import Path
from dotenv import load_dotenv

# === 讀取環境變數 ===
load_dotenv()

# === 基本路徑設定 ===
BASE_DIR = Path(__file__).resolve().parent.parent

# === 安全設定 ===
SECRET_KEY = os.getenv('SECRET_KEY', 'your-dev-secret-key')  # 保險起見
DEBUG = True
ALLOWED_HOSTS = []

# === 已安裝的 App ===
INSTALLED_APPS = [
    # Django 內建
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 🌈 Planora 的主要模組
    'apps.core',       # ✅ 共用模板與首頁
    # 'apps.timeline',   # ✅ 團體共編行事曆
    'apps.personal',   # ✅ 個人行事曆
    #'apps.meetings',   # ✅ 會議記錄
    'apps.accounts',
]

# === 中介層 ===
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# === URL ===
ROOT_URLCONF = 'config.urls'

# === 模板設定 ===
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ✅ 若未來有全域模板可放這裡
        'APP_DIRS': True,  # ✅ 會自動尋找各 app 下的 /templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# === WSGI ===
WSGI_APPLICATION = 'config.wsgi.application'

# === 資料庫設定 ===
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# === 密碼驗證 ===
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# === 語言與時區 ===
LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True

# === 靜態檔案 ===
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# === 媒體檔案（使用者上傳） ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'uploads'

# === 預設主鍵型態 ===
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === 登入 / 登出導向設定 ===
LOGIN_REDIRECT_URL = 'core:home'     # 登入後導回首頁
LOGOUT_REDIRECT_URL = 'core:home'    # 登出後導回首頁
LOGIN_URL = 'accounts:login'          # 若有用 allauth 登入系統