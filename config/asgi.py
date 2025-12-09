"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os
from django.core.asgi import get_asgi_application

# ⚠️ 部署用的 settings，注意不能用 development
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Django ASGI 入口
application = get_asgi_application()



