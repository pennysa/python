from django.db import models
from django.conf import settings


# ============================
# 📁 Folder
# ============================
class TreeFolder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="treedoc_folders"
    )
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ============================
# 📄 Document（屬於 Folder）
# ============================
class TreeDocument(models.Model):
    folder = models.ForeignKey(
        TreeFolder,
        on_delete=models.CASCADE,
        related_name="documents",
        null=True,      # ⭐ 允許舊資料為空
        blank=True
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="treedocs"
    )

    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    head_version = models.ForeignKey(
        "TreeVersion",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="head_of"
    )

    def __str__(self):
        return self.title



# ============================
# 🌿 Version Tree
# ============================
class TreeVersion(models.Model):
    document = models.ForeignKey(
        TreeDocument,
        on_delete=models.CASCADE,
        related_name="versions"
    )

    parent = models.ForeignKey(
        "self",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    branch_name = models.CharField(max_length=100, default="main")
    message = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to="treedoc_files/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.document.title} | {self.branch_name}"


