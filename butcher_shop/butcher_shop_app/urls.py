from django.urls import path
from .views import index, registrations, user_login, user_logout, shopping_cart

urlpatterns = [
    path("", index),
    path("registrations", registrations),
    path("login", user_login),
    path("logout", user_logout),
    path("shopping_cart", shopping_cart),
]
