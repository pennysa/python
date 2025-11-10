from django.db import models

class Event(models.Model):
    # 🩵 基本資訊
    title = models.CharField("事件標題", max_length=100)
    note = models.TextField("備註", blank=True)

    # ⏰ 時間設定
    start = models.DateTimeField("開始時間")
    end = models.DateTimeField("結束時間", null=True, blank=True)

    # 🎨 使用者從固定色票挑選的顏色
    color = models.CharField(
        "顏色代碼",
        max_length=20,
        default="#93c5fd",
        help_text="由使用者從固定色票挑選（8 色）"
    )

    # 🏷 標籤（可有可無）
    tag = models.CharField(
        "分類標籤",
        max_length=50,
        blank=True,
        help_text="例如：學業、運動、生活"
    )

    # ⚡ 優先順序（用於近七天 TODO 排序）
    priority = models.CharField(
        "優先順序",
        max_length=10,
        choices=[("低", "低"), ("中", "中"), ("高", "高")],
        default="中"
    )

    # ✅ 是否完成（會讓事件變灰色＋刪除線）
    is_completed = models.BooleanField("是否完成", default=False)

    # 📆 建立與更新時間
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "個人事件"
        verbose_name_plural = "個人行事曆事件"
        ordering = ["start"]

    def __str__(self):
        return f"{self.title}（{self.start.strftime('%Y-%m-%d')}）"

    # ✅ 回傳要給 FullCalendar 顯示的顏色（完成時固定灰色）
    @property
    def display_color(self):
        if self.is_completed:
            return "#d1d5db"  # 灰色
        return self.color

