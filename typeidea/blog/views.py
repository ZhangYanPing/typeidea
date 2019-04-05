from django.shortcuts import render

from django.http import HttpResponse
from .models import Tag, Category, Post


def post_list(request, category_id=None, tag_id=None):
    ''' content = 'post_list category_id={category_id}, tag_id={tag_id}'.format(
         category_id=category_id,
         tag_id=tag_id,
     )
     return HttpResponse(content)'''
    # return render(request, 'blog/list.html', context={'name': 'post_list'})

    tag = None
    category = None
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_post()

    context = {
        'category': category,
        'tag': tag,
        'post_list': post_list,
    }
    context.update(Category.get_navs())

    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id=None):
    # return HttpResponse('detail')
    # return render(request, 'blog/detail.html', context={'name': 'post_detail'})
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    context = {
        'post': post,
    }
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
