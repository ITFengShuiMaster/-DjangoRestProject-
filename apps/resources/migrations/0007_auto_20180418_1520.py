# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-18 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0006_auto_20180418_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmodel',
            name='file_size',
            field=models.CharField(default='', help_text='文件大小统计', max_length=20, verbose_name='文件大小统计'),
        ),
    ]
