from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, GoodsInShoppingCart, ProductCategories, UserAdditionalInfo, Order, OrderItems
from .forms import ApplicationForm, UserRegistrationsForm, UserLoginForm, UserAdditionalInfoForm, OrderForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


def index(request):
    context = {}

    products = Product.objects.all()[:4]
    form = ApplicationForm()
    context['products'] = products
    context["form"] = form

    return render(request, "butcher_shop_app/index.html", context)


def send_application(request):
    if request.method == "POST":
        print("Я был здесь!!!")
        form = ApplicationForm(request.POST)
        form.save()
    return HttpResponse("Я был здесь!!!")


def add_to_cart(request):
    product_id = int(request.POST.get("product_id", "0"))
    print(product_id)
    count = int(request.POST.get("count", "0"))
    if not request.user.is_authenticated:
        product = request.POST.get("product_name", "")
        add_to_shopping_cart(request, product_id, count, product)
        is_success = True
    else:
        added_product = {'id': product_id, 'count': count}
        user_cart_in_def_cart = GoodsInShoppingCart.objects.filter(user=request.user)
        add_old_products_to_log_cart(added_product, user_cart_in_def_cart, request.user)
        is_success = True
    if is_success:
        return HttpResponse("Добавление в корзину прошло успешно")


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
    context = cart_logic(request)
    return render(request, "butcher_shop_app/shopping_cart.html", context)


def cart_logic(request):
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
    context.update(get_cart_sum_count_kgs(request))
    return context


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
            if product['id'] == int(product_id):
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
            if product['id'] == int(product_id):
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
            if product['id'] == int(product_id):
                product.clear()
        while {} in cure_shopping_cart_dict:
            cure_shopping_cart_dict.remove({})
        request.session['shopping_cart'] = cure_shopping_cart_dict


def add_to_shopping_cart(request, id: int, count: int, product: str):
    if not request.session.get('shopping_cart'):
        request.session['shopping_cart'] = []
    is_in_list = 0
    cost = Product.objects.get(id=id).cost
    cure_shopping_cart_dict = request.session['shopping_cart']
    for i in cure_shopping_cart_dict:
        if i['id'] == id:
            is_in_list = 1

            i['count'] += count
            i['cost'] = cost
            i['total_cost'] = i['count'] * i['cost']
    if not is_in_list:
        print("был здесь")
        a = {"id": id, 'count': count, 'product': product, 'cost': cost, "total_cost": cost * count}
        print(a)
        cure_shopping_cart_dict.append(
            {"id": id, 'count': count, 'product': product, 'cost': cost, "total_cost": cost * count})
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
    # if request.method == "POST":
    #   add_to_cart(request)
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


def order_create_view(request):
    context = {}
    context.update(get_cart_sum_count_kgs(request))
    form = init_order_form(request)
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            create_order(request, form)
            context["order_send_status"] = 1
            form = init_order_form(request)
        else:
            context["errors"] = form.errors
            form = OrderForm(request.POST)
    if context["product_count"]:
        context["form"] = form
    else:
        context["add_product_in_cart"] = "Для заказа, добавьте товары в корзину, пожалуйста"
    context.update(cart_logic(request))
    return render(request, "butcher_shop_app/order_create.html", context)


def get_cart_sum_count_kgs(request):
    cart_info = {}
    products_count_kg = 0
    total_cost = 0
    count = 0
    if request.user.is_authenticated:
        cart = GoodsInShoppingCart.objects.filter(user=request.user)
        for product in cart:
            count += 1
            products_count_kg += product.count
            total_cost += products_count_kg * product.product.cost
    else:
        cart = request.session.get("shopping_cart", [])
        for product in cart:
            count += 1
            products_count_kg += product["count"]
            product_cost = Product.objects.get(id=product["id"]).cost
            total_cost += products_count_kg * product_cost
    cart_info["products_count_kg"] = products_count_kg
    cart_info["total_cost"] = total_cost
    cart_info["product_count"] = count
    return cart_info


def get_order_info(order):
    """Принимается объект Order"""
    items = OrderItems.objects.filter(order_id=order)
    result = {}
    total_items = 0
    total_cost = 0
    total_kgs = 0
    for item in items:
        total_items += 1
        cure_kgs = item.product_count
        total_kgs += cure_kgs
        total_cost += item.product_id.cost * cure_kgs
    result["total_items"] = total_items
    result["total_cost"] = total_cost
    result["total_kgs"] = total_kgs
    return result


def create_order(request, form):
    order_id = gen_order_id(request)
    order = form.save(commit=False)
    if request.user.is_authenticated:
        order.user = request.user
    order.my_id = order_id
    order.created = date.today()
    order.save()
    from_cart_to_order(request, order_id)
    dell_cart_after_order(request)
    order = Order.objects.get(my_id=order_id)
    order_info_dict = get_order_info(order)
    order.total_cost = order_info_dict["total_cost"]
    order.total_items = order_info_dict["total_items"]
    order.total_kgs = order_info_dict["total_kgs"]
    order.save()


def init_order_form(request):
    initial_dict = {}
    if request.user.is_authenticated:
        user = UserAdditionalInfo.objects.get(user=request.user)
        user_base = User.objects.get(username=request.user)
        phone_number = user.phone_number
        address = user.address
        name = user_base.first_name
        if phone_number:
            initial_dict["phone_number"] = phone_number
        if address:
            initial_dict["address"] = address
        if name:
            initial_dict["name"] = name
    form = OrderForm(initial_dict)
    return form


def gen_order_id(request):
    order_id = str(date.today())
    order_id += str(request.user)
    order_id += str(len(Order.objects.filter(created=date.today())) + 1)
    return order_id


def from_cart_to_order(request, order_id):
    order = Order.objects.get(my_id=order_id)
    if request.user.is_authenticated:
        # Если пользователь авторизован
        # перекидываем товары из корзины в бд в orderItems
        cart = GoodsInShoppingCart.objects.filter(user=request.user)
        for product in cart:
            product_id = product.product
            product_count = product.count
            order_item = OrderItems(order_id=order, product_id=product_id, product_count=product_count)
            order_item.save()
    else:
        # Иначе перекидываем из сессий
        cart = request.session.get("shopping_cart", [])
        for product in cart:
            product_id = Product.objects.get(id=product["id"])
            product_count = int(product["count"])
            order_item = OrderItems(order_id=order, product_id=product_id, product_count=product_count)
            order_item.save()


def dell_cart_after_order(request):
    if request.user.is_authenticated:
        cart = GoodsInShoppingCart.objects.filter(user=request.user)
        for product in cart:
            product.delete()
    else:
        request.session["shopping_cart"] = []


@login_required(login_url='http://127.0.0.1:8000/login')
def lk_view(request):
    context = {}
    # корзина
    context.update(get_cart_sum_count_kgs(request))
    cart = GoodsInShoppingCart.objects.filter(user=request.user)
    context["cart"] = cart
    context["cart_len"] = len(cart)
    # заказы
    orders = Order.objects.filter(user=request.user)
    context["orders"] = orders
    context["orders_len"] = len(orders)
    return render(request, "butcher_shop_app/lk.html", context)
