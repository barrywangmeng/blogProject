# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()

    create_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    # 文章摘要 可以没有文章摘要，因为CharField 默认情况下要求必须存入数据
    # 指定CharField的blank=True参数值后就可以允许空值了
    excerpt = models.CharField(max_length=200, blank=True)

    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有很多文章，所以使用ForeignKey即代表一对多的关系
    # 文章和标签是多对多的关系，所以使用ManyToManyField
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    # 这里的User是从django.contrib.auth.modles导入的
    # django.contrib.auth是Django内置的引用，专门用于处理网站用户的注册、登录等流程
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    # 自定义 get_absolute_url 方法
    # 记得从 django.urls 中导入 reverse 函数
    def get_absolute_url(self):
        # reverse 函数
        return reverse('blog:detail', kwargs={'pk': self.pk})