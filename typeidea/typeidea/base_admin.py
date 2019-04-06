from django.contrib import admin


class BaseOwnerAdmin(admin.ModelAdmin):
    """
    1. 用来自动补充文章，分类，标签，到边栏，友链这些Model的owner字段
    2. 用来针对queryset过滤当前用户的数据
    """
    exclude = ('owner',)

    def save_model(self, request, obj, form, change):
        print('save model in BaseOwnerAdmin')
        obj.owner = request.user
        return super(BaseOwnerAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        print('base owner admin --')
        print(request.user)
        qs = super(BaseOwnerAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)
