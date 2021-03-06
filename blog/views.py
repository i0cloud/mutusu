import markdown
from datetime import date
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache

from .models import Category, Tag, Article


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'allcatetories': Category.objects.all(),
            'alltags': Tag.objects.all(),
        })
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Article.latest_articles()
    paginate_by = 10
    context_object_name = 'article_list'
    template_name = 'blog/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hot_articles"] = Article.objects.all().order_by('-pv')[0:5]
        return context
    


class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class SearchView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["keyword"] = self.request.GET.get('keyword', '')
        return context
    
    def get_queryset(self):
        queryset =  super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
    

class ArticleDetailView(CommonViewMixin, DetailView):
    queryset = Article.latest_articles()
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        # ?????? get_object ????????????????????????????????? article ??? content ???????????????
        article = super(ArticleDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                              'markdown.extensions.extra',
                              'markdown.extensions.codehilite',
                              'markdown.extensions.toc',
                              ])
        article.content = md.convert(article.content)
        article.toc = md.toc
        return article
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_visited()
        return response
    
    def handle_visited(self):
        increase_pv = False
        increase_uv = False
        uid = self.request.uid
        pv_key = 'pv:%s:%s' % (uid, self.request.path)
        uv_key = 'uv:%s:%s:%s' % (uid, str(date.today()), self.request.path)
        if not cache.get(pv_key):
            increase_pv = True
            cache.set(pv_key, 1, 1 * 60)    # 1????????????
        
        if not cache.get(uv_key):
            increase_uv = True
            cache.set(uv_key, 1, 24 * 60 * 60)    # 24????????????
        
        if increase_pv and increase_uv:
            Article.objects.filter(pk=self.object.id).update(pv=F('pv') + 1, uv=F('uv') + 1)
        elif increase_pv:
            Article.objects.filter(pk=self.object.id).update(pv=F('pv') + 1)
        elif increase_uv:
            Article.objects.filter(pk=self.object.id).update(uv=F('uv') + 1)