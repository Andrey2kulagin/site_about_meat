from django.urls import path
from .views import index, registrations, user_login, user_logout, shopping_cart, product_list, product_detail, \
    order_create_view, lk_view, add_to_cart, send_application, goods_count_minus_plus

urlpatterns = [
    path("", index, name="index"),
    path("registrations", registrations, name="registrations"),
    path("login", user_login, name="login"),
    path("logout", user_logout, name="logout"),
    path("shopping_cart", shopping_cart, name="shopping_cart"),
    path("product_list", product_list, name="product_list"),
    path("product_detail/<int:pk>", product_detail, name="product_detail"),
    path("order_create", order_create_view, name="order_create"),
    path("add_to_cart", add_to_cart, name="add_to_cart"),
    path("lk", lk_view, name="lk"),
    path("send_application", send_application, name="send_application"),
    path("goods_count_minus_plus/<int:pk>", goods_count_minus_plus, name="goods_count_minus_plus"),

]
