from django.contrib import admin
from .models import Dataset, ChartConfig, AnalysisResult

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'upload_date']
    search_fields = ['name']

@admin.register(ChartConfig)
class ChartConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'chart_type', 'x_axis', 'y_axis', 'color', 'line_style']
    list_filter = ['chart_type']

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'dataset', 'created_at']
