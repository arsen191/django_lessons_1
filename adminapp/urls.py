from django.urls import path
from adminapp import views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('users/create/', adminapp.user_create, name='user_create'),
    path('users/read/', adminapp.users, name='users'),
    path('users/update/<int:pk>/', adminapp.user_update, name='user_update'),
    path('users/delete/<pk>/', adminapp.user_delete, name='user_delete'),

    path('category/create/', adminapp.category_create, name='category_create'),
    path('category/read/', adminapp.categories, name='categories'),
    path('category/update/<pk>/', adminapp.category_update, name='category_update'),
    path('category/delete/<pk>/', adminapp.category_delete, name='category_delete'),

    path('product/create/category/<pk>/', adminapp.product_create, name='product_create'),
    path('product/read/category/<pk>/', adminapp.products, name='products'),
    path('product/read/<pk>/', adminapp.product_read, name='product_read'),
    path('product/update/<pk>/', adminapp.product_update, name='product_update'),
    path('product/delete/<pk>/', adminapp.product_delete, name='product_delete'),
]
