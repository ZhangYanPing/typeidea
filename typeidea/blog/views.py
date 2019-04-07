from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView

from django.http import HttpResponse
from .models import Tag, Category, Post
from config.models import Link, SideBar


class CommonViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        }
        )
        context.update(Category.get_navs())
        return context


class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_post()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class CategoryView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        '''重写qauery set, 根据过滤器分类'''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写qauery set, 根据标签分类'''
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)


class PostDetailView(CommonViewMixin, DetailView):
    queryset = Post.latest_post()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'


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
    context.update({'sidebars': SideBar.get_all()})

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
    context.update({'sidebars': SideBar.get_all()})
    context.update(Category.get_navs())
    return render(request, 'blog/detail.html', context=context)
