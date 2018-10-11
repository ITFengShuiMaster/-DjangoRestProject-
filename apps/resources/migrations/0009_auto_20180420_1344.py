# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-20 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0008_auto_20180420_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='textmodel',
            name='file_type',
            field=models.CharField(choices=[('docx', 'word文档'), ('pptx', 'ppt文档'), ('xlsx', 'excel文档'), ('pdf', 'pdf文档')], default='docx', help_text='上传文件的格式', max_length=20, verbose_name='上传文件的格式'),
        ),
    ]
