from django.shortcuts import render

links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classics', 'name': 'классика'},
        ]


def main(request):
    content = {
        'title': 'Главная'
    }
    return render(request, 'mainapp/index.html', content)


def contact(request):
    content = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', content)


def product(request):
    content = {
        'title': 'Продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_all(request):
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_home(request):
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_office(request):
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_modern(request):
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)


def products_classics(request):
    content = {
        'title': 'продукты',
        'links_menu': links_menu,
    }
    return render(request, 'mainapp/products.html', content)
