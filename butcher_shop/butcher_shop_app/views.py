from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, GoodsInShoppingCart, ProductCategories
from .forms import ApplicationForm, UserRegistrationsForm, UserLoginForm, UserAdditionalInfoForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    context = {}

    products = Product.objects.all()
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == 'application':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                form.save()
        elif form_type == 'shopping_cart':
            add_to_cart(request)
    form = ApplicationForm()
    context['products'] = products
    context["form"] = form

    return render(request, "butcher_shop_app/index.html", context)


def add_to_cart(request):
    product_id = int(request.POST.get("product_id", "0"))
    count = int(request.POST.get("count", "0"))
    if not request.user.is_authenticated:
        product = request.POST.get("product_name", "")
        add_to_shopping_cart(request, product_id, count, product)
    else:
        added_product = {'id': product_id, 'count': count}
        user_cart_in_def_cart = GoodsInShoppingCart.objects.filter(user=request.user)
        add_old_products_to_log_cart(added_product, user_cart_in_def_cart, request.user)


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
            cart_from_session_for_login(request, user)
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
            cart_from_session_for_login(request, user)
            next_str = request.GET.get("next", "")
            return redirect("http://127.0.0.1:8000" + next_str)
        else:
            context["errors"] = login_form.errors
    login_form = UserLoginForm()
    context["login_form"] = login_form
    return render(request, "butcher_shop_app/login.html", context)


def user_logout(request):
    logout(request)
    next_str = request.GET.get("next", "")
    return redirect("http://127.0.0.1:8000" + next_str)


def shopping_cart(request):
    context = {}
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "goods_count_minus":
            goods_count_minus_plus(request, -1)
        if form_type == 'goods_count':
            change_goods_count(request)
        if form_type == 'goods_count_plus':
            goods_count_minus_plus(request, 1)
        if form_type == 'del_good':
            del_good(request)
    if request.user.is_authenticated:
        user_cart = GoodsInShoppingCart.objects.filter(user=request.user)
        context["cart"] = user_cart
        context["count_goods_in_cart"] = len(user_cart)
    else:
        shopping_cart_eq = request.session.get('shopping_cart', [])
        count_goods_in_cart = len(shopping_cart_eq)
        context["cart"] = shopping_cart_eq
        context["count_goods_in_cart"] = count_goods_in_cart
    return render(request, "butcher_shop_app/shopping_cart.html", context)


def goods_count_minus_plus(request, change):
    product_id = request.POST.get("product_id")
    if request.user.is_authenticated:
        product = GoodsInShoppingCart.objects.get(id=product_id)
        product.count += change
        product.save()
    else:
        if not request.session.get('shopping_cart'):
            request.session['shopping_cart'] = []
        cure_shopping_cart_dict = request.session['shopping_cart']
        for product in cure_shopping_cart_dict:
            if product['id'] == product_id:
                product['count'] += change
        request.session['shopping_cart'] = cure_shopping_cart_dict


def change_goods_count(request):
    product_id = request.POST.get("product_id")
    new_goods_count = int(request.POST.get("goods_count"))
    if request.user.is_authenticated:
        product = GoodsInShoppingCart.objects.get(id=product_id)
        product.count = new_goods_count
        product.save()
    else:
        if not request.session.get('shopping_cart'):
            request.session['shopping_cart'] = []
        cure_shopping_cart_dict = request.session['shopping_cart']
        for product in cure_shopping_cart_dict:
            if product['id'] == product_id:
                product['count'] = new_goods_count
        request.session['shopping_cart'] = cure_shopping_cart_dict


def del_good(request):
    product_id = request.POST.get("product_id")
    if request.user.is_authenticated:
        product = GoodsInShoppingCart.objects.get(id=product_id)
        product.delete()
    else:
        if not request.session.get('shopping_cart'):
            request.session['shopping_cart'] = []
        cure_shopping_cart_dict = request.session['shopping_cart']
        for product in cure_shopping_cart_dict:
            if product['id'] == product_id:
                del product
        request.session['shopping_cart'] = cure_shopping_cart_dict


def add_to_shopping_cart(request, id: int, count: int, product: str):
    if not request.session.get('shopping_cart'):
        request.session['shopping_cart'] = []
    is_in_list = 0
    cure_shopping_cart_dict = request.session['shopping_cart']
    for i in cure_shopping_cart_dict:
        if i['id'] == id:
            is_in_list = 1
            i['count'] += count
    if not is_in_list:
        cure_shopping_cart_dict.append({"id": id, 'count': count, 'product': product})
    request.session['shopping_cart'] = cure_shopping_cart_dict


def cart_from_session_for_login(request, user):
    products_in_session_cart = request.session.get('shopping_cart', '')
    if products_in_session_cart == '':
        return 0
    user_cart_in_def_cart = GoodsInShoppingCart.objects.filter(user=user)
    if len(user_cart_in_def_cart):
        for session_product in products_in_session_cart:
            add_old_products_to_log_cart(session_product, user_cart_in_def_cart, user)
    else:
        for session_product in products_in_session_cart:
            add_new_product_to_log_cart(session_product, user)


def add_new_product_to_log_cart(session_product, user):
    product = get_object_or_404(Product, id=session_product['id'])
    new_product = GoodsInShoppingCart(user=user, product=product, count=session_product['count'])
    new_product.save()


def add_old_products_to_log_cart(added_product: dict, user_cart_in_def_cart, user):
    is_in_cart = 0
    for product_in_log_cart in user_cart_in_def_cart:
        if product_in_log_cart.product.id == added_product["id"]:
            is_in_cart = 1
            product_in_log_cart.count += added_product['count']
            product_in_log_cart.save()
    if not is_in_cart:
        add_new_product_to_log_cart(added_product, user)


def product_list(request):
    context = {}
    user_categories = request.GET.getlist("category", None)
    if user_categories:
        selected_categories = ProductCategories.objects.filter(category_name__in=user_categories)
        products = Product.objects.filter(category_name__in=selected_categories)
    else:
        products = Product.objects.all()
    if request.method == "POST":
        add_to_cart(request)
    categories = ProductCategories.objects.all()
    context["categories"] = categories
    context["products"] = products
    return render(request, "butcher_shop_app/product_list.html", context)


def product_detail(request, pk):
    context = {}
    product = get_object_or_404(Product, id=pk)
    context['product'] = product
    if request.method == "POST":
        add_to_cart(request)
    return render(request, 'butcher_shop_app/product_detail.html', context)


def order_create(request):
    pass