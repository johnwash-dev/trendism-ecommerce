from django.urls import path
from . import views

urlpatterns = [
    path('category/<slug:category_slug>/', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]