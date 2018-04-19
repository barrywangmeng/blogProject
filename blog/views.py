# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import markdown

from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render
from .models import Post

def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    post.body = markdown.markdown(post.body,['extra', 'codehilite', 'toc', ])
    return render(request, 'blog/detail.html', context={'post':post})