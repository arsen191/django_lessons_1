import random

from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page

from basketapp.models import Basket
from mainapp.models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_hot_product():
    product_list = Product.objects.filter(category__is_active=True, is_active=True)
    return random.sample(list(product_list), 1)[0]


def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3].select_related()


def main(request):
    products = Product.objects.all()[:3].select_related()
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


def prod(request, pk):
    title = 'продукты'
    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk)
    }
    return render(request, 'mainapp/product.html', content)


# @cache_page(3600)
def product(request, pk=None, page=1):
    links_menu = get_links_menu()

    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user).select_related()

    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            product_list = Product.objects.all()
        else:
            category = get_category(pk)
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
