# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/14 21:23'

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import TextModel

import os


class TextFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_text(self, text):
        text_records = TextModel.objects.filter(text__contains=text.name)
        if text_records:
            raise serializers.ValidationError("上传文件名已存在")
        return text

    def validate_file_type(self, file_type):
        text = self.initial_data['text']
        text_name = text.name
        upload_file_type = text_name[text_name.rfind(r'.')+1:]
        if upload_file_type != file_type:
            if upload_file_type != 'doc':
                raise serializers.ValidationError("上传文件格式不正确")
        return file_type

    def validate(self, attrs):
        return attrs

    class Meta:
        model = TextModel
        fields = ['id', 'user', 'text', 'text_type', 'file_type']


class TextFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextModel
        fields = ['id', 'text', 'text_type', 'file_type', 'file_size', 'file_name', 'pdf_path']
