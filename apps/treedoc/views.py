#from django.shortcuts import render, get_object_or_404, redirect
#from django.contrib.auth.decorators import login_required
#from django.http import JsonResponse
#from django.contrib import messages

#from .models import Folder, Document


# ============================
# 📁 資料夾列表（根目錄）
# ============================
# @login_required
# def folder_list(request):
#     folders = Folder.objects.filter(
#         user=request.user,
#         parent__isnull=True
#     )
#     return render(request, "treedoc/folder_list.html", {
#         "folders": folders
#     })


# # ============================
# # 📁 資料夾內容（子資料夾 + 文件）
# # ============================
# @login_required
# def folder_detail(request, folder_id):
#     folder = get_object_or_404(
#         Folder,
#         id=folder_id,
#         user=request.user
#     )

#     subfolders = folder.children.all()
#     documents = folder.documents.all()

#     return render(request, "treedoc/folder_detail.html", {
#         "folder": folder,
#         "subfolders": subfolders,
#         "documents": documents,
#     })


# # ============================
# # ➕ 新增資料夾
# # ============================
# @login_required
# def create_folder(request):
#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()
#         parent_id = request.POST.get("parent")

#         if not name:
#             messages.error(request, "資料夾名稱不能是空的")
#             return redirect("treedoc:folder_list")

#         parent = None
#         if parent_id:
#             parent = Folder.objects.filter(
#                 id=parent_id,
#                 user=request.user
#             ).first()

#         Folder.objects.create(
#             user=request.user,
#             parent=parent,
#             name=name
#         )

#         messages.success(request, "資料夾已建立")

#         if parent:
#             return redirect("treedoc:folder_detail", folder_id=parent.id)
#         return redirect("treedoc:folder_list")

#     return redirect("treedoc:folder_list")


# # ============================
# # ✏️ 重新命名資料夾
# # ============================
# @login_required
# def rename_folder(request, folder_id):
#     folder = get_object_or_404(
#         Folder,
#         id=folder_id,
#         user=request.user
#     )

#     if request.method == "POST":
#         new_name = request.POST.get("name", "").strip()
#         if new_name:
#             folder.name = new_name
#             folder.save()
#             messages.success(request, "資料夾名稱已更新")

#     return redirect("treedoc:folder_detail", folder_id=folder.id)


# # ============================
# # ❌ 刪除資料夾（含內容）
# # ============================
# @login_required
# def delete_folder(request, folder_id):
#     folder = get_object_or_404(
#         Folder,
#         id=folder_id,
#         user=request.user
#     )

#     parent = folder.parent
#     folder.delete()
#     messages.success(request, "資料夾已刪除")

#     if parent:
#         return redirect("treedoc:folder_detail", folder_id=parent.id)
#     return redirect("treedoc:folder_list")


# # ============================
# # 📄 上傳文件（檔案 + 附註）
# # ============================
# @login_required
# def upload_document(request, folder_id):
#     folder = get_object_or_404(
#         Folder,
#         id=folder_id,
#         user=request.user
#     )

#     if request.method == "POST":
#         file = request.FILES.get("file")
#         note = request.POST.get("note", "").strip()

#         if not file:
#             messages.error(request, "請選擇檔案")
#             return redirect("treedoc:folder_detail", folder_id=folder.id)

#         Document.objects.create(
#             user=request.user,
#             folder=folder,
#             file=file,
#             note=note
#         )

#         messages.success(request, "文件已上傳")
#         return redirect("treedoc:folder_detail", folder_id=folder.id)

#     return redirect("treedoc:folder_detail", folder_id=folder.id)


# ============================
# ❌ 刪除文件
# ============================
#@login_required
#def delete_document(request, doc_id):
#    doc = get_object_or_404(
 #       Document,
 #       id=doc_id,
 #       user=request.user
 #   )

 #   folder_id = doc.folder.id
 #   doc.file.delete(save=False)
 #   doc.delete()

 #   messages.success(request, "文件已刪除")
 #   return redirect("treedoc:folder_detail", folder_id=folder_id)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def treedoc_placeholder(request):
    return render(request, "treedoc/placeholder.html")
