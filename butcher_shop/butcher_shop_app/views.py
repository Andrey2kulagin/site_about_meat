from django.shortcuts import render

def index(request):
    return render(request,"butcher_shop_app/index.html")

