# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/13 09:35'

from django.db.models.signals import post_save
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from .models import UserPointLove, VideoComment, VideoCommentReplyModel, UserFavVideo
from courses.models import FileVideoModel

import datetime


@receiver(post_save, sender=UserPointLove)
def create_UserPointLove(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            if instance.reply_type == 1:
                video_com = VideoComment.objects.get(id=instance.video_comment)
                video_com.point_love_nums += 1
                video_com.save()
            else:
                video_com = VideoCommentReplyModel.objects.get(id=instance.video_comment)
                video_com.point_love_nums += 1
                video_com.save()
        except:
            pass


@receiver(post_delete, sender=UserPointLove)
def delete_UserPointLove(sender, instance=None, **kwargs):
    try:
        if instance.reply_type == 1:
            video_com = VideoComment.objects.get(id=instance.video_comment)
            video_com.point_love_nums -= 1
            video_com.save()
        else:
            video_com = VideoCommentReplyModel.objects.get(id=instance.video_comment)
            video_com.point_love_nums -= 1
            video_com.save()
    except:
        pass


@receiver(post_save, sender=UserFavVideo)
def create_UserFavVideo(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            video = FileVideoModel.objects.get(id=instance.video_id)
            video.fav_num += 1
            video.save()
        except:
            pass


@receiver(post_delete, sender=UserFavVideo)
def delete_UserFavVideo(sender, instance=None, **kwargs):
    try:
        video = FileVideoModel.objects.get(id=instance.video_id)
        video.fav_num -= 1
        video.save()
    except:
        pass