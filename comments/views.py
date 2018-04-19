# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import markdown
from django.shortcuts import render, get_object_or_404, redirect
from .models import Comment
from .forms import CommentForm
from blog.models import Post


# Create your views here.

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        # django 自动检查表单的数据是否符合格式要求
        if form.is_valid():
            # 将表单数据保存到数据库中
            # commit=False的作用是仅仅利用表单数据生成Comment模型类的实例，但并不保存数据到数据库
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来
            comment.post = post

            # 最终保存到db中
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = post.comment_set.all()
            context = {'post':post, 'form':form, 'comment_list':comment_list}

            return render(request, 'blog/detail.html', context=context)

    return redirect(post)


def detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.body = markdown.markdown(post.body,
                          extensions=[
                              'markdown.extensions.extra',
                              'markdown.extensions.codehilite',
                              'markdown.extensions.toc',
                          ])
    form = CommentForm()
    comment_list = post.comment_set.all()

    context = {'post':post, 'form':form, 'comment_list':comment_list}
    return render(request, 'blog/detail.html', context=context)