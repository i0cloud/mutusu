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

from blog.views import article_list, article_detail

urlpatterns = [
    re_path('^$', article_list, name='index'),
    re_path('^article/(?P<article_id>\d+).html$', article_detail, name='article-detail'),
    re_path('^category/(?P<category_id>\d+)/$', article_list, name='category-list'),
    re_path('^tag/(?P<tag_id>\d+)/$', article_list, name='tag-list'),
    path('admin/', admin.site.urls),
    re_path('meditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)