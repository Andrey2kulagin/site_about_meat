from django.urls import path
from .views import index, registrations, user_login, user_logout, shopping_cart, product_list, product_detail

urlpatterns = [
    path("", index),
    path("registrations", registrations),
    path("login", user_login),
    path("logout", user_logout),
    path("shopping_cart", shopping_cart),
    path("product_list", product_list),
    path("product_detail/<int:pk>", product_detail),
]
