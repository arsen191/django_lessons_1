import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    return []


def get_hot_product():
    product_list = Product.objects.all()
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]


def main(request):
    products = Product.objects.all()[:3]
    content = {
        'title': 'Главная',
        'products': products,
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', content)


def prod(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', content)


def product(request, pk=None, page=1):
    links_menu = ProductCategory.objects.all()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            product_list = Product.objects.all()
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            product_list = Product.objects.filter(category__pk=pk)

        paginator = Paginator(product_list, 2)
        try:
            product_paginator = paginator.page(page)
        except PageNotAnInteger:
            product_paginator = paginator.page(1)
        except EmptyPage:
            product_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': 'Продукты',
            'category': category,
            'product_list': product_paginator,
            'links_menu': links_menu,
            'basket': basket
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
        'same_products': same_products,
        'basket': basket,
        'hot_product': hot_product
    }
    return render(request, 'mainapp/products.html', content)

