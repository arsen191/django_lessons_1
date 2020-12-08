from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import Product


def basket(request):
    return render(request,)


def add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket_item = Basket.objects.filter(user=request.user, product=product).first()
    if not basket_item:
        basket_item = Basket(user=request.user, product=product)
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete(request, pk):
    pass
