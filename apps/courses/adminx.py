# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/11 21:22'

from xadmin import views
import xadmin

from .models import FileVideoModel


class FileVideoAdmin(object):

    list_diplay = ['user', 'video_name', 'desc', 'video_img', 'click_num', 'fav_num', 'video_kind', 'url', 'add_time']
    search_fields = ['user', 'video_name', 'desc', 'video_img', 'click_num', 'fav_num', 'video_kind', 'url']
    list_filter = ['user', 'video_name', 'desc', 'video_img', 'click_num', 'fav_num', 'video_kind', 'url', 'add_time']


xadmin.site.register(FileVideoModel, FileVideoAdmin)