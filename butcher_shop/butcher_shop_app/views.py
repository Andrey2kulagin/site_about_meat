from django.shortcuts import render
from .models import Product
from .forms import ApplicationForm


def index(request):
    products = Product.objects.all()
    form = ApplicationForm()
    context = {'products': products, "form": form}
    return render(request, "butcher_shop_app/index.html", context)
