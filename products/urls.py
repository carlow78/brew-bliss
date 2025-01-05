from django.urls import path
from . import views
from .views import all_products, product_detail, add_product, edit_product, delete_product, add_review 

urlpatterns = [
    
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),

]