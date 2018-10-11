# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-27 15:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0026_auto_20180427_1530'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocommentreplymodel',
            name='is_love',
            field=models.BooleanField(default=False, help_text='是否点过赞', verbose_name='是否点过赞'),
        ),
        migrations.AddField(
            model_name='videocommentreplymodel',
            name='point_love_nums',
            field=models.IntegerField(default=0, help_text='点赞数', verbose_name='点赞数'),
        ),
    ]
