from django.shortcuts import render
from .models import Product


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "butcher_shop_app/index.html", context)
