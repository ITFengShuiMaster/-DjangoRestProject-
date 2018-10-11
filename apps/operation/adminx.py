# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/12 19:32'

import xadmin

from .models import VideoComment, UserPointLove, UserFavVideo


class VideoCommentAdmin(object):
    list_diplay = ['user', 'video', 'comment', 'com_type', 'parent_comment', 'add_time', 'point_love_nums']
    search_fields = ['user', 'video', 'comment', 'com_type', 'parent_comment', 'point_love_nums']
    list_filter = ['user', 'video', 'comment', 'com_type', 'parent_comment', 'add_time', 'point_love_nums']


class UserPointLoveAdmin(object):
    list_diplay = ['user', 'video_comment', 'add_time']
    search_fields = ['user', 'video_comment']
    list_filter = ['user', 'video_comment', 'add_time']


class UserFavVideoAdmin(object):
    list_diplay = ['user', 'video', 'add_time']
    search_fields = ['user', 'video']
    list_filter = ['user', 'video', 'add_time']


xadmin.site.register(VideoComment, VideoCommentAdmin)
xadmin.site.register(UserPointLove, UserPointLoveAdmin)
xadmin.site.register(UserFavVideo, UserFavVideoAdmin)
