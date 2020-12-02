"""django_framework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    path('contact/', mainapp.contact, name='contact'),
    path('product/', mainapp.product, name='product'),
    path('product/all/', mainapp.products_all, name='products_all'),
    path('product/home/', mainapp.products_home, name='products_home'),
    path('product/office/', mainapp.products_office, name='products_office'),
    path('product/modern/', mainapp.products_modern, name='products_modern'),
    path('product/classics/', mainapp.products_classics, name='products_classics'),

    path('admin/', admin.site.urls),
]
