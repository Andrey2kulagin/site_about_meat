from django.urls import path
from .views import index, registrations, user_login, user_logout

urlpatterns = [
    path("", index),
    path("registrations", registrations),
    path("login", user_login),
    path("logout", user_logout),
]
