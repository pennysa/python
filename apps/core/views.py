# apps/core/views.py

from django.shortcuts import render
from django.contrib import messages

def home(request):
    """
    網站首頁
    展示系統介紹與功能說明
    """
        # 檢查是否剛登出
    if 'logout' in request.GET:
        messages.success(request, "已成功登出 👋 歡迎下次再來！")
    return render(request, 'core/home.html')