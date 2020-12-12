from django.urls import path
from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.product, name='index'),
    path('<int:pk>/', mainapp.product, name='category'),
    path('prod/<int:pk>/', mainapp.prod, name='prod'),
]
