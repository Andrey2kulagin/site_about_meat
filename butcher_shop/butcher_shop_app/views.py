from django.shortcuts import render, redirect
from .models import Product
from .forms import ApplicationForm, UserRegistrationsForm, UserLoginForm, UserAdditionalInfoForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    products = Product.objects.all()
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
    form = ApplicationForm()
    context = {'products': products, "form": form}
    return render(request, "butcher_shop_app/index.html", context)


def registrations(request):
    context = {}
    if request.method == "POST":
        reg_form = UserRegistrationsForm(request.POST)
        additional_info_form = UserAdditionalInfoForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            additional_info = additional_info_form.save(commit=False)
            additional_info.user = user
            additional_info.save()
            login(request, user)
            next_str = request.GET.get("next", "")
            return redirect("http://127.0.0.1:8000" + next_str)
        else:
            context["errors"] = reg_form.errors
    reg_form = UserRegistrationsForm()
    additional_info_form = UserAdditionalInfoForm()
    context["reg_form"] = reg_form
    context["add_info_form"] = additional_info_form
    return render(request, "butcher_shop_app/registrations.html", context)


def user_login(request):
    context = {}
    if request.method == "POST":
        login_form = UserLoginForm(data=request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            next_str = request.GET.get("next", "")
            return redirect("http://127.0.0.1:8000"+next_str)
        else:
            context["errors"] = login_form.errors
    login_form = UserLoginForm()
    context["login_form"] = login_form
    return render(request, "butcher_shop_app/login.html", context)


def user_logout(request):
    logout(request)
    next_str = request.GET.get("next", "")
    return redirect("http://127.0.0.1:8000"+next_str)


@login_required(login_url='http://127.0.0.1:8000/login')
def shopping_cart(request):
    return render(request, "butcher_shop_app/shopping_cart.html")
