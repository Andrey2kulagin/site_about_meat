from django.shortcuts import render, get_object_or_404
from django.apps import apps
from .models import Blog
Product = apps.get_model('butcher_shop_app', 'Product')


def blog_list(request):
    context = {}
    posts = Blog.objects.filter(is_receipt=False)
    context['posts'] = posts
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, id):
    context = {}
    post = get_object_or_404(Blog, id=id)
    context['post'] = post
    products = Product.objects.all()[0:4]
    context["products_block"] = products
    return render(request, 'blog/blog_detail.html', context)


def receipt_list(request):
    context = {}
    posts = Blog.objects.filter(is_receipt=True)
    context['posts'] = posts
    return render(request, 'blog/blog_list.html', context)
