from django.urls import path
from . import views

urlpatterns = [
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/add/', views.sale_add, name='sale_add'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/<int:pk>/delete/', views.sale_delete, name='sale_delete'),
]