# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-11 00:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20180411_0013'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='nick_name',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='nick_name',
            field=models.CharField(default='', help_text='昵称', max_length=20, verbose_name='昵称'),
        ),
    ]
