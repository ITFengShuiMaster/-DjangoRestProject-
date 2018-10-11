# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/5/16 14:34'

import xadmin

from .models import TaskModel


class TaskModelAdmin(object):

    list_diplay = ['user', 'title', 'content', 'mession_kind', 'point_nums', 'attention_nums', 'task_level', 'add_times']
    search_fields = ['user', 'title', 'content', 'mession_kind', 'point_nums', 'attention_nums', 'task_level']
    list_filter = ['user', 'title', 'content', 'mession_kind', 'point_nums', 'attention_nums', 'task_level', 'add_times']

xadmin.site.register(TaskModel, TaskModelAdmin)


