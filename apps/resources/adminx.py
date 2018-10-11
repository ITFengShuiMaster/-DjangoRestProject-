# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/14 21:14'

from .models import TextModel

import xadmin


class TextFileAdmin(object):
    list_diplay = ['user', 'text', 'text_type', 'file_type', 'download_nums', 'add_time']
    search_fields = ['user', 'text', 'text_type', 'file_type', 'download_nums']
    list_filter = ['user', 'text', 'text_type', 'file_type', 'download_nums', 'add_time']

xadmin.site.register(TextModel, TextFileAdmin)
