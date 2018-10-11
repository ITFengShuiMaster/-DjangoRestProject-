# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/8 16:22'

from xadmin import views
import xadmin

from .models import UserInfo, VerifyCode


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = '智慧农业产学研后台管理系统'
    site_footer = '@智慧农业产学研后台管理系统'
    menu_style = 'accordion'


class UserInfoAdmin(object):

    list_diplay = ['user', 'image', 'birth', 'sex', 'address', 'address', 'add_time']
    search_fields = ['user', 'image', 'birth', 'sex', 'address', 'address']
    list_filter = ['user', 'image', 'birth', 'sex', 'address', 'address', 'add_time']


class VerifyCodeAdmin(object):
    list_diplay = ['mobile', 'code', 'add_time']
    search_fields = ['mobile', 'code']
    list_filter = ['mobile', 'code', 'add_time']

xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(UserInfo, UserInfoAdmin)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)