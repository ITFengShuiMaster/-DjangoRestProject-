# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-20 15:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0015_useruploadfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useruploadfile',
            name='text',
            field=models.ForeignKey(help_text='上传文档', on_delete=django.db.models.deletion.CASCADE, related_name='texts', to='resources.TextModel', verbose_name='上传文档'),
        ),
    ]
