from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# ✅ 允許 GET 顯示登出確認頁
class LogoutConfirmView(LogoutView):
    http_method_names = ['get', 'post', 'head']
    template_name = 'account/logout.html'

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutConfirmView.as_view(), name='logout'),
]
