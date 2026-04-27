from django.urls import path
from . import views

urlpatterns = [
    path('stitching/', views.stitching_list, name='stitching_list'),
    path('stitching/add/', views.stitching_add, name='stitching_add'),
    path('stitching/edit/<int:pk>/', views.stitching_edit, name='stitching_edit'),
    path('stitching/delete/<int:pk>/', views.stitching_delete, name='stitching_delete'),
]