# from django.urls import path
# from . import views

# app_name = "treedoc"

# urlpatterns = [

#     # =========================
#     # 📁 Folder
#     # =========================
#     path(
#         "",
#         views.folder_list,
#         name="folder_list"
#     ),

#     path(
#         "folder/create/",
#         views.create_folder,
#         name="create_folder"
#     ),

#     path(
#         "folder/<int:folder_id>/",
#         views.folder_detail,
#         name="folder_detail"
#     ),

#     path(
#         "folder/<int:folder_id>/rename/",
#         views.rename_folder,
#         name="rename_folder"
#     ),

#     path(
#         "folder/<int:folder_id>/delete/",
#         views.delete_folder,
#         name="delete_folder"
#     ),

#     # =========================
#     # 📄 Document
#     # =========================
#     path(
#         "folder/<int:folder_id>/upload/",
#         views.upload_document,
#         name="upload_document"
#     ),

#     path(
#         "doc/<int:doc_id>/delete/",
#         views.delete_document,
#         name="delete_document"
#     ),
# ]

from django.urls import path
from . import views

app_name = "treedoc"

urlpatterns = [
    path("", views.treedoc_placeholder, name="placeholder"),
]

