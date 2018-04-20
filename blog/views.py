# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render

from comments.forms import CommentForm
from .models import Post, Category

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context=context)

# 根据年月信息找出对应的文章数据
def archives(request, year, month):
    # 这个地方create_time__year 是代码自动补全的
    # Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表
    # 所以 Django 要求我们把点替换成了两个下划线，即 created_time__year
    post_list = Post.objects.filter(create_time__year=year, create_time__month=month).order_by('-create_time')
    return render(request, "blog/index.html", context={'post_list':post_list})

def category(request, pk):
    category = get_object_or_404(Category, pk = pk)
    post_list = Post.objects.filter(category=category).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})