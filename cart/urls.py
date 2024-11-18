from django.urls import path
from . import views

urlpatterns = [

    path('', views.view_cart, name='view_cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('modify/<int:item_id>/', views.modify_cart, name='modify_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart,
         name='remove_from_cart'),

]

