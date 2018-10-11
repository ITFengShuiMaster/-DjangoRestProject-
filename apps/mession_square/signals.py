# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/5/15 16:35'

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.response import Response
from rest_framework import status

from .models import TaskModel, TaskReplyModel, UserAttentionTask, TaskPointModel, TaskReplyComment,\
    TaskReplyCommentReplyModel


@receiver(post_save, sender=TaskReplyModel)
def create_TaskReplyModel(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            task = TaskModel.objects.get(id=instance.task_id)
            task.reply_nums += 1
            task.save()
        except Exception as e:
            print(e)


@receiver(post_save, sender=UserAttentionTask)
def create_UserAttentionTask(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            task = TaskModel.objects.get(id=instance.task_id)
            task.attention_nums += 1
            task.save()
        except Exception as e:
            print(e)


@receiver(post_delete, sender=UserAttentionTask)
def delete_UserAttentionTask(sender, instance=None, **kwargs):
    try:
        task = TaskModel.objects.get(id=instance.task_id)
        task.attention_nums -= 1
        task.save()
    except Exception as e:
        print(e)


@receiver(post_save, sender=TaskPointModel)
def create_TaskPointModel(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            to_id_type = instance.to_id_type
            obj = None
            if to_id_type == 1:
                obj = TaskReplyModel.objects.get(id=instance.to_id)
                obj.point_nums += 1
            elif to_id_type == 2:
                obj = TaskReplyComment.objects.get(id=instance.to_id)
                obj.point_nums += 1
            else:
                obj = TaskReplyCommentReplyModel.objects.get(id=instance.to_id)
                obj.point_nums += 1
            obj.save()
        except Exception as e:
            return Response({"detail":"没有该条记录"}, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_delete, sender=TaskPointModel)
def delete_TaskPointModel(sender, instance=None, **kwargs):
    try:
        to_id_type = instance.to_id_type
        obj = None
        if to_id_type == 1:
            obj = TaskReplyModel.objects.get(id=instance.to_id)
            obj.point_nums -= 1
        elif to_id_type == 2:
            obj = TaskReplyComment.objects.get(id=instance.to_id)
            obj.point_nums -= 1
        else:
            obj = TaskReplyCommentReplyModel.objects.get(id=instance.to_id)
            obj.point_nums -= 1
        obj.save()
    except Exception as e:
        print(e)


@receiver(post_save, sender=TaskReplyComment)
def create_TaskReplyComment(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            obj = TaskReplyModel.objects.get(id=instance.task_reply_id)
            obj.comment_nums += 1
            obj.save()
        except Exception as e:
            return Response({"detail":"没有该条记录"}, status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=TaskReplyCommentReplyModel)
def create_TaskReplyCommentReplyModel(sender, instance=None, created=False, **kwargs):
    if created:
        try:
            obj = TaskReplyComment.objects.get(id=instance.comment_id_id)
            obj.comment_nums += 1
            obj.save()
        except Exception as e:
            return Response({"detail":"没有该条记录"}, status=status.HTTP_400_BAD_REQUEST)