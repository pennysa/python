from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages    # ⭐ 你之前漏掉這個
from .models import TreeFolder, TreeDocument, TreeVersion


# ============================
# 📁 Folder List
# ============================
@login_required
def folder_list(request):
    folders = TreeFolder.objects.filter(user=request.user)
    return render(request, "treedoc/folder_list.html", {"folders": folders})


# ============================
# 📁 Folder Detail（顯示文件）
# ============================
@login_required
def folder_detail(request, folder_id):
    folder = get_object_or_404(TreeFolder, id=folder_id, user=request.user)
    return render(request, "treedoc/folder_detail.html", {
        "folder": folder,
        "documents": folder.documents.all(),
    })


# ============================
# ➕ 在 Folder 裡建立 Document
# ============================
@login_required
def create_document(request, folder_id):
    folder = get_object_or_404(TreeFolder, id=folder_id, user=request.user)

    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            doc = TreeDocument.objects.create(
                user=request.user,
                folder=folder,
                title=title,
            )
            return redirect("treedoc:document_detail", doc_id=doc.id)

    return redirect("treedoc:folder_detail", folder_id=folder.id)


# ============================
# 📄 Document Detail（版本列表）
# ============================
@login_required
def document_detail(request, doc_id):
    doc = get_object_or_404(TreeDocument, id=doc_id, user=request.user)
    versions = doc.versions.order_by("created_at")

    return render(request, "treedoc/document_detail.html", {
        "doc": doc,
        "versions": versions,
    })


# ============================
# ⬆️ Upload Version Page
# ============================
@login_required
def upload_page(request, doc_id):
    doc = get_object_or_404(TreeDocument, id=doc_id, user=request.user)
    return render(request, "treedoc/upload_page.html", {"doc": doc})


# ============================
# ⬆️ Upload Version（正式修正版）
# ============================
@login_required
def upload_version(request, doc_id):
    doc = get_object_or_404(TreeDocument, id=doc_id, user=request.user)

    if request.method == "POST":
        file = request.FILES.get("file")              # ⭐ 一定要用 request.FILES
        message = request.POST.get("message", "")
        branch = request.POST.get("branch_name", "main")
        content = request.POST.get("content", "")

        parent_id = request.POST.get("parent")
        parent = TreeVersion.objects.filter(id=parent_id).first() if parent_id else None

        version = TreeVersion.objects.create(
            document=doc,
            user=request.user,
            file=file,
            branch_name=branch,
            message=message,
            content=content,
            parent=parent,
        )

        # 更新最新版
        doc.head_version = version
        doc.save()

        messages.success(request, "版本已成功上傳！")
        return redirect("treedoc:document_detail", doc_id=doc.id)

    return redirect("treedoc:upload_page", doc_id=doc.id)


# ============================
# 🌳 Version Tree JSON
# ============================
@login_required
def version_tree_json(request, doc_id):
    doc = get_object_or_404(TreeDocument, id=doc_id, user=request.user)
    versions = doc.versions.all()

    def build(v):
        return {
            "id": v.id,
            "branch": v.branch_name,
            "message": v.message,
            "created_at": v.created_at.strftime("%Y-%m-%d %H:%M"),
            "file": v.file.url if v.file else None,
            "children": [build(child) for child in v.children.all()],
        }

    roots = versions.filter(parent__isnull=True)
    return JsonResponse([build(v) for v in roots], safe=False)


# ============================
# 📁 建立資料夾（Ajax）
# ============================
@login_required
def create_folder(request):
    if request.method == "POST":
        name = request.POST.get("name")
        folder = TreeFolder.objects.create(user=request.user, name=name)
        return JsonResponse({"success": True, "id": folder.id, "name": folder.name})

    return JsonResponse({"success": False})

