from django.db import models
from django.contrib.auth.models import User    # 使用Django自带的用户模型

from mdeditor.fields import MDTextField


# 文章分类
class Category(models.Model):
    name = models.CharField('名称', max_length=20, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '分类'

# 文章标签
class Tag(models.Model):
    name = models.CharField('名称', max_length=20, unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '标签'

#文章
class Article(models.Model):
    title = models.CharField('标题', max_length=200)
    desc = models.CharField('摘要', max_length=1024, blank=True)
    content = MDTextField('正文')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name='标签')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    pv = models.PositiveIntegerField(default=1)    # 页面访问量，即PageView
    uv = models.PositiveIntegerField(default=1)    # 独立访问用户数，即UniqueVisitor
    
    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag = None
            article_list = []
        else:
            article_list = tag.article_set.all()
        
        return tag, article_list
    
    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            article_list = None
        else:
            article_list = category.article_set.all()
        
        return category, article_list
    
    @classmethod
    def latest_articles(cls):
        queryset = cls.objects.all()
        return queryset

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-created_time']