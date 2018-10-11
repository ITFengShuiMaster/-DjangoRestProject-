# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-16 16:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mession_square', '0004_auto_20180516_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskReplyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='回答内容', verbose_name='回答内容')),
                ('add_times', models.DateField(default=datetime.datetime.now, help_text='创建时间', verbose_name='创建时间')),
                ('task', models.ForeignKey(help_text='回答的问题', on_delete=django.db.models.deletion.CASCADE, related_name='task_reply', to='mession_square.TaskModel', verbose_name='回答的问题')),
                ('user', models.ForeignKey(help_text='回答用户', on_delete=django.db.models.deletion.CASCADE, related_name='task_reply_user', to=settings.AUTH_USER_MODEL, verbose_name='回答用户')),
            ],
            options={
                'verbose_name': '提问表',
                'verbose_name_plural': '提问表',
            },
        ),
    ]
