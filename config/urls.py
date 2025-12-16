from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 🏠 Core / Home
    path('', include(('apps.core.urls', 'core'), namespace='core')),

    # 📅 Personal Calendar
    path('personal/', include(('apps.personal.urls', 'personal'), namespace='personal')),

    # 🔐 Accounts（Email / Google 登入）
    path('accounts/', include('allauth.urls')),
    path('accounts/', include(('apps.accounts.urls', 'accounts'), namespace='accounts')),

    # 🌳 Treedoc — must include namespace !!!
    path('treedoc/', include(('apps.treedoc.urls', 'treedoc'), namespace='treedoc')),

    # ⚙ Django Admin
    path('admin/', admin.site.urls),
]

# 📂 Media file serving
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
