# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-12 21:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0007_commentlove'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentlove',
            name='video',
            field=models.OneToOneField(help_text='评论', on_delete=django.db.models.deletion.CASCADE, related_name='video_love', to='operation.VideoComment', verbose_name='评论'),
        ),
    ]
