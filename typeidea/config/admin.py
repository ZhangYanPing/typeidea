from django.contrib import admin

from .models import Link, SideBar
from typeidea.custome_site import custom_site
from typeidea.base_admin import BaseOwnerAdmin


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'created_time')
    fields = ('title', 'href', 'status', 'weight')


@admin.register(SideBar, site=custom_site)
class SiderBarAdmin(BaseOwnerAdmin):
    print('side bar admin')
    list_display = ('title', 'display_type', 'content', 'created_time')
    fields = ('title', 'display_type', 'content')
