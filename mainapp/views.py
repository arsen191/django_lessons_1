from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def main(request):
    products = Product.objects.all()[:3]
    content = {
        'title': 'Главная',
        'products': products
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', content)


def product(request, pk=None):
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            product_list = Product.objects.all()
        else:
            # category = ProductCategory.objects.get(pk=pk)
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=pk)

        content = {
            'title': 'Продукты',
            'category': category,
            'product_list': product_list,
            'links_menu': links_menu,
            'basket': basket
        }
        return render(request, 'mainapp/products_list.html', content)

    same_products = Product.objects.all()[2:5]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket
    }
    return render(request, 'mainapp/products.html', content)

