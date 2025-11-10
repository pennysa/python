from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🌈 首頁與共用頁面
    path('', include('apps.core.urls')),  # ✅ 改回 include，交給 core/urls.py 管理

    # 🪄 個人行事曆
    path('personal/', include('apps.personal.urls')),

    # ⚙️ 管理後台
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
