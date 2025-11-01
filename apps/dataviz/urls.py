from django.urls import path
from . import views

urlpatterns = [
    path('', views.dataviz_index, name='dataviz_index'),
]
