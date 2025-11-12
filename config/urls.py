from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('apps.core.urls')),        # ✅ 登入 / 登出 / 首頁
    path('personal/', include('apps.personal.urls')),  # ✅ 個人行事曆
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),        # ✅ 加這行！啟用 Google / GitHub / Email 登入
    path('accounts/', include('apps.accounts.urls')),  # ✅ 登入登出由 accounts 處理

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
