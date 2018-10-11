# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/11 21:01'

from rest_framework import serializers

from .models import FileTestModel, FileVideoModel
from users.serializers import UserProfileSerializer


class FileTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTestModel
        fields = ['video_name', 'video']


class ListVideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileVideoModel
        fields = ['id', 'video_name', 'desc', 'video_img', 'click_num', 'video_kind']


class RetrieveVideoFileSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = FileVideoModel
        fields = ['id', 'video_name', 'desc', 'video_img', 'click_num', 'video_kind', 'url', 'video_file', 'user']


class CreateVideoFileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = FileVideoModel
        fields = ['user', 'video_name', 'desc', 'video_img', 'video_kind', 'url', 'video_file']