"""mutusu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from blog.views import IndexView, CategoryView, TagView, ArticleDetailView, SearchView


urlpatterns = [
    re_path('^$', IndexView.as_view(), name='index'),
    re_path('^article/(?P<article_id>\d+).html$', ArticleDetailView.as_view(), name='article-detail'),
    re_path('^category/(?P<category_id>\d+)/$', CategoryView.as_view(), name='category-list'),
    re_path('^tag/(?P<tag_id>\d+)/$', TagView.as_view(), name='tag-list'),
    re_path('^search/$', SearchView.as_view(), name='search'),
    path('admin/', admin.site.urls),
    re_path('mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)