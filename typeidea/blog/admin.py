from django.contrib import admin

from .models import Post, Category, Tag
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm
from typeidea.custom_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin
from django.contrib.admin.models import LogEntry


class PostInline(admin.TabularInline):
    fields = ('title', 'desc')
    extra = 1
    model = Post


class CategoryOwnerFilter(admin.SimpleListFilter):
    ''' 自定义过滤器只显示当前用户分类 '''
    title = '分类过滤器'
    parameter_name = 'owner_category'
    # parameter_name = 'category_id__exact'

    def lookups(self, request, mode_admin):
        return Category.objects.filter(owner=request.user).values_list('id', 'name')
        ''' return (
             (1, 'IT 技术'),
             (2, '随笔'),
         )
         '''

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())
        return queryset


@admin.register(Category, site=custom_site)
class CategoryAdmin(BaseOwnerAdmin):
    #print('category admin')
    inlines = [PostInline, ]
    list_display = ('name', 'status', 'is_nav', 'owner', 'post_count')
    fields = ('name', 'status', 'is_nav')

    def post_count(self, obj):
        return obj.post_set.count()

    post_count.short_description = '文章数量'


@admin.register(Tag, site=custom_site)
class TagAdmin(BaseOwnerAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')


@admin.register(Post, site=custom_site)
class PostAdmin(BaseOwnerAdmin):
    form = PostAdminForm
    # filter_vertical = ('tag', )  # not working
    filter_horizontal = ('tag', )  # not working
    list_display = ['title', 'category', 'status', 'created_time', 'owner', 'operator']
    list_display_links = []
    list_filter = [CategoryOwnerFilter, ]
    # list_filter = ['category', ]
    search_fields = ['title', 'category_name']

    actions_on_top = True
    actions_on_bottom = True

    # 编辑页面
    save_on_top = True
    '''
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )'''

    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields': (
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容', {
            'fields': (
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes': ('collapse',),
            'fields': ('tag', ),
        })
    )

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('cus_admin:blog_post_change', args=(obj.id,))
        )

    operator.short_description = '操作'

    '''
    class Media:
        css = {
            'all': ("https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/bootstrap.min.css",),
        }
        js = ('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)
    '''


@admin.register(LogEntry, site=custom_site)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['object_repr', 'object_id', 'action_flag', 'user', 'change_message']
