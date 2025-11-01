import pandas as pd
import chardet
from django.shortcuts import render
from .models import Dataset, AnalysisResult


def dataviz_index(request):
    context = {}

    if request.method == "POST" and request.FILES.get("data_file"):
        file = request.FILES["data_file"]

        # === 自動偵測編碼 ===
        raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result["encoding"]

        # 重新定位檔案指標
        file.seek(0)

        try:
            df = pd.read_csv(file, encoding=encoding)
        except Exception as e:
            context["error"] = f"❌ 檔案讀取錯誤：{str(e)}"
            return render(request, "dataviz/index.html", context)

        # === 儲存 Dataset 紀錄 ===
        dataset = Dataset.objects.create(
            name=file.name,
            file_path=file
        )

        # === 自動摘要統計（強化版） ===
        try:
            summary = df.describe(include='all', datetime_is_numeric=True).transpose()

            # 若完全沒有數值欄，改為類別統計
            if summary.empty:
                summary = pd.DataFrame({
                    "欄位名稱": df.columns,
                    "唯一值數量": [df[c].nunique() for c in df.columns],
                    "最常出現值": [df[c].mode().iloc[0] if not df[c].mode().empty else "-" for c in df.columns],
                    "最常出現次數": [df[c].value_counts().iloc[0] if not df[c].value_counts().empty else "-" for c in df.columns],
                })
                summary_html = summary.to_html(classes="table table-bordered table-sm", index=False)
            else:
                # === 中文化欄位名稱 ===
                summary = summary.fillna("")
                summary.index.name = "欄位名稱"
                summary.columns = summary.columns.map({
                    "count": "非缺失值數",
                    "unique": "唯一值數量",
                    "top": "最常出現值",
                    "freq": "最常出現次數",
                    "mean": "平均數",
                    "std": "標準差",
                    "min": "最小值",
                    "25%": "第1四分位",
                    "50%": "中位數",
                    "75%": "第3四分位",
                    "max": "最大值"
                }).fillna(summary.columns)
                summary_html = summary.to_html(classes="table table-bordered table-sm", na_rep="-")

            # 儲存到資料庫（JSON）
            AnalysisResult.objects.create(
                dataset=dataset,
                summary_json=summary.to_dict()
            )

            context["summary"] = summary_html

        except Exception as e:
            context["summary_error"] = f"⚠️ 自動摘要統計失敗：{str(e)}"

        # === 缺失值統計 ===
        missing = df.isnull().sum().reset_index()
        missing.columns = ["欄位名稱", "缺失值數量"]
        missing_html = missing.to_html(classes="table table-sm table-hover", index=False)
        context["missing"] = missing_html

        # === 儲存顯示內容 ===
        context["uploaded"] = True
        context["columns"] = df.columns.tolist()
        context["preview"] = df.head(10).to_html(classes="table table-striped table-sm", index=False)
        context["message"] = f"✅ 成功上傳「{file.name}」，自動偵測編碼為 {encoding}"

        # === 檔案資訊卡顯示 ===
        context["file_name"] = file.name
        try:
            context["upload_time"] = dataset.created_at.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            context["upload_time"] = "未知"

        context["encoding"] = encoding

        try:
            context["file_size"] = f"{round(file.size / 1024, 2)} KB"
        except Exception:
            context["file_size"] = "未知"

        # === 暫存於 session 供繪圖使用 ===
        request.session["data"] = df.to_json(orient="records")

    return render(request, "dataviz/index.html", context)
