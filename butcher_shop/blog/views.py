from django.shortcuts import render, get_object_or_404
from .models import Blog


def blog_list(request):
    context = {}
    posts = Blog.objects.all()
    context['posts'] = posts
    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, id):
    context = {}
    post = get_object_or_404(Blog, id=id)
    context['post'] = post
    return render(request, 'blog/blog_detail.html', context)
