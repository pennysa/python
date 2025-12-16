from django.urls import path
from . import views

app_name = "treedoc"

urlpatterns = [
    # folder level
    path("folders/", views.folder_list, name="folder_list"),
    path("folder/<int:folder_id>/", views.folder_detail, name="folder_detail"),
    path("folder/<int:folder_id>/new_doc/", views.create_document, name="create_document"),

    # document level
    path("doc/<int:doc_id>/", views.document_detail, name="document_detail"),

    # version upload
    path("doc/<int:doc_id>/upload/", views.upload_page, name="upload_page"),
    path("doc/<int:doc_id>/upload/save/", views.upload_version, name="upload_version"),

    # version tree json
    path("doc/<int:doc_id>/tree/", views.version_tree_json, name="version_tree_json"),

    # create folder
    path("folder/create/", views.create_folder, name="create_folder"),

]

