import markdown
from django.shortcuts import render

from .models import Category, Tag, Article


def article_list(request, category_id=None, tag_id=None):
    allcatetories = Category.objects.all()
    category = None
    tag = None

    if tag_id:
        tag, article_list = Article.get_by_tag(tag_id)
    elif category_id:
        category, article_list = Article.get_by_category(category_id)
    else:
        article_list = Article.latest_articles()
    context = {
        'allcatetories': allcatetories,
        'category': category,
        'tag': tag,
        'article_list': article_list,
    }
    return render(request, 'blog/list.html', context)

def article_detail(request, article_id):
    allcatetories = Category.objects.all()

    try:
        article = Article.objects.get(id=article_id)
        tags = article.tag.all()
        article.content = markdown.markdown(
            article.content, extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
    except Article.DoesNotExist:
        article = None
    
    context = {
        'allcatetories': allcatetories,
        'article': article,
        'tags': tags,
    }
    return render(request, 'blog/detail.html', context)