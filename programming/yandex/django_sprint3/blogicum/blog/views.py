from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from datetime import datetime
from django.http import Http404

from .models import Post, Category


# Create your views here.
def index(request):
    """
    Главная страница

    Returns:
       Отображение списка постов
    """
    posts = (
        Post.objects.select_related("category")
        .filter(pub_date__lt=datetime.now())
        .filter(is_published=True)
        .filter(category__is_published=True)
        .order_by("-pub_date"))[0:5]
    context = {"post_list": posts}
    return render(request, "blog/index.html", context)


def post_detail(request, id):
    """
    Детали поста

    Args:
        id (int): Айдишник страницы
    Returns:
        Отображение страницы с деталями поста
    """
    post = get_object_or_404(
        Post.objects.select_related("category")
        .filter(
            Q(pub_date__lt=datetime.now())
            & Q(is_published=True)
            & Q(category__is_published=True)
        ),
        id=id
    )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    """
    Посты из категории

    Args:
        category_slug (str): Слаг категории
    Returns:
        Отображение страницы с постами из конкретной категории
    """
    category = Category.objects.get(slug=category_slug)
    if not category.is_published:
        raise Http404("Такой категории не существует")
    category_posts = (
        Post.objects
        .select_related("category")
        .filter(category__slug=category_slug)
        .filter(is_published=True)
        .filter(pub_date__lt=datetime.now())
    )

    context = {"post_list": category_posts, "category": category}
    return render(request, "blog/category.html", context)
