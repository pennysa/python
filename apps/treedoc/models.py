from django.db import models
from django.conf import settings


# ============================
# 📁 Folder（可巢狀）
# ============================
class Folder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="folders"
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children"
    )

    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================
# 📄 Document（一個檔案）
# ============================
class Document(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    file = models.FileField(upload_to="documents/")
    note = models.CharField(
        max_length=300,
        blank=True,
        help_text="文件附註（像 GitHub commit message）"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.file.name
