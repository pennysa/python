from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 

class Event(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,    # ← 這裡才是正確的！
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 🩵 基本資訊
    title = models.CharField("事件標題", max_length=100)
    note = models.TextField("備註", blank=True)

    # ⏰ 時間設定
    start = models.DateTimeField("開始時間")
    end = models.DateTimeField("結束時間", null=True, blank=True)

    # 🎨 顏色
    color = models.CharField(
        "顏色代碼",
        max_length=20,
        default="#93c5fd",
        help_text="由使用者從固定色票挑選（8 色）"
    )

    # 🏷 標籤
    tag = models.CharField(
        "分類標籤",
        max_length=50,
        blank=True,
        help_text="例如：學業、運動、生活"
    )

    # ⚡ 優先順序
    priority = models.CharField(
        "優先順序",
        max_length=10,
        choices=[("低", "低"), ("中", "中"), ("高", "高")],
        default="中"
    )

    # ✅ 完成狀態
    is_completed = models.BooleanField("是否完成", default=False)

    # 📆 建立／更新時間
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "個人事件"
        verbose_name_plural = "個人行事曆事件"
        ordering = ["start"]

    def __str__(self):
        return f"{self.title}（{self.start.strftime('%Y-%m-%d')}）"

    # FullCalendar 顯示顏色
    @property
    def display_color(self):
        if self.is_completed:
            return "#d1d5db"
        return self.color


