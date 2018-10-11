# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 19:18
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0003_auto_20180411_2210'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(help_text='评论内容', max_length=150, verbose_name='评论内容')),
                ('com_type', models.IntegerField(choices=[(1, '一级评论'), (2, '二级评论')], default=1, help_text='评论级别', verbose_name='评论级别')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('parent_comment', models.ForeignKey(help_text='父级评论', on_delete=django.db.models.deletion.CASCADE, related_name='parent_com', to='operation.VideoComment', verbose_name='父级评论')),
                ('user', models.ForeignKey(help_text='评论用户', on_delete=django.db.models.deletion.CASCADE, related_name='video_user_comment', to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
                ('video', models.ForeignKey(help_text='所评论的视频', on_delete=django.db.models.deletion.CASCADE, related_name='video_file_comment', to='courses.FileVideoModel', verbose_name='所评论的视频')),
            ],
            options={
                'verbose_name': '评论表',
                'verbose_name_plural': '评论表',
            },
        ),
    ]
