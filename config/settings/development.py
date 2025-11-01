from .base import *
import os
from dotenv import load_dotenv
import dj_database_url

# 載入 .env 檔案
load_dotenv()


DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# 使用 DATABASE_URL 設定資料庫
DATABASES = {
    'default': dj_database_url.parse(
        os.getenv('DATABASE_URL'),
        conn_max_age=600  # 連線池:連線最多保持 600 秒(10分鐘)
    )
}



from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# 開發環境使用 SQLite
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
