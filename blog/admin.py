from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Tag, Article

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','article_count', 'created_time')
    fields = ('name', )

    def article_count(self, obj):
        return obj.article_set.count()
    article_count.short_description = "文章数量"

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_time')
    fields = ('name', )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'category', 'created_time', 'operator')
    list_display_links = None

    list_filter = ['category', 'created_time']
    search_fields = ['title', 'category__name']
    
    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'fields': ('tag',),
        })
    )
    filter_horizontal = ('tag',)

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_article_change', args=(obj.id,))
        )
    operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(ArticleAdmin, self).save_model(request, obj, form, change)