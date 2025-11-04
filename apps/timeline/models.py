from django.db import models

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('學習', '學習'),
        ('工作', '工作'),
        ('生活', '生活'),
    ]

    title = models.CharField(max_length=100)  # 任務標題
    category = models.CharField(              # 分類
        max_length=10,
        choices=CATEGORY_CHOICES,
        default='生活'
    )
    description = models.TextField(blank=True)  # 任務描述（可留空）
    start_date = models.DateField()              # 開始日期
    end_date = models.DateField(null=True, blank=True)  # 結束日期（可留空）
    is_done = models.BooleanField(default=False)  # 是否完成

    def __str__(self):
        return f"{self.title} ({self.category})"

