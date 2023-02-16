from django.shortcuts import render, redirect
from .models import Product
from .forms import ApplicationForm, UserRegistrationsForm, UserLoginForm
from django.contrib.auth import login, logout


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
        if reg_form.is_valid():
            reg_form.save()
        else:
            context["errors"] = reg_form.errors
    reg_form = UserRegistrationsForm()
    context["reg_form"] = reg_form
    return render(request, "butcher_shop_app/registrations.html", context)


def user_login(request):
    context = {}
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("http://127.0.0.1:8000/")
        else:
            context["errors"] = login_form.errors
    login_form = UserLoginForm()
    context["login_form"] = login_form
    return render(request, "butcher_shop_app/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("http://127.0.0.1:8000/")
