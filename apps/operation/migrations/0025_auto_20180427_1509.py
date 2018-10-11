# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-27 15:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0024_auto_20180427_1438'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TestReplyModel',
            new_name='VideoCommentReplyModel',
        ),
        migrations.RemoveField(
            model_name='testvideocommentmodel',
            name='user',
        ),
        migrations.RemoveField(
            model_name='testvideocommentmodel',
            name='video',
        ),
        migrations.AlterModelOptions(
            name='videocomment',
            options={'verbose_name': '二级评论表', 'verbose_name_plural': '二级评论表'},
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='com_type',
        ),
        migrations.RemoveField(
            model_name='videocomment',
            name='parent_comment',
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='user',
            field=models.ForeignKey(help_text='评论用户', on_delete=django.db.models.deletion.CASCADE, related_name='test_video_user_comment', to=settings.AUTH_USER_MODEL, verbose_name='评论用户'),
        ),
        migrations.AlterField(
            model_name='videocomment',
            name='video',
            field=models.ForeignKey(help_text='所评论的视频', on_delete=django.db.models.deletion.CASCADE, related_name='test_video_file_comment', to='courses.FileVideoModel', verbose_name='所评论的视频'),
        ),
        migrations.AlterField(
            model_name='videocommentreplymodel',
            name='comment_id',
            field=models.ForeignKey(help_text='根评论', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_com', to='operation.VideoComment', verbose_name='根评论'),
        ),
        migrations.DeleteModel(
            name='TestVideoCommentModel',
        ),
    ]
