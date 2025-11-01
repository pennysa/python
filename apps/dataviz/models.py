from django.db import models

class Dataset(models.Model):
    """記錄使用者上傳的資料集"""
    name = models.CharField(max_length=100, verbose_name="資料名稱")
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name="上傳時間")
    file_path = models.FileField(upload_to='uploads/', verbose_name="檔案路徑")

    def __str__(self):
        return self.name


class ChartConfig(models.Model):
    """使用者選擇的圖表設定"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='charts')
    chart_type = models.CharField(max_length=50, verbose_name="圖表類型", default='line')
    x_axis = models.CharField(max_length=50, verbose_name="X軸欄位")
    y_axis = models.CharField(max_length=200, verbose_name="Y軸欄位（多選）")
    color = models.CharField(max_length=20, default="#007bff", verbose_name="顏色")
    line_style = models.CharField(max_length=20, default="solid", verbose_name="線條樣式")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"{self.dataset.name} - {self.chart_type}"


class AnalysisResult(models.Model):
    """自動摘要統計或分組統計結果"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='analyses')
    summary_json = models.JSONField(verbose_name="摘要統計（JSON）")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="建立時間")

    def __str__(self):
        return f"{self.dataset.name} 的統計結果"
