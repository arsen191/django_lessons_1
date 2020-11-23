from django.shortcuts import render


def main(request):
    return render(request, 'mainapp/index.html')


def contact(request):
    return render(request, 'mainapp/contact.html')


def product(request):
    return render(request, 'mainapp/products.html')
