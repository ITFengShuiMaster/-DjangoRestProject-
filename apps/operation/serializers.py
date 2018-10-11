# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/12 19:18'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from .models import UserPointLove, UserFavVideo, UserUploadFile, VideoComment, VideoCommentReplyModel, UserFavMession
from resources.serializers import TextFileSerializer
from users.serializers import UserProfileSerializer
from courses.serializers import RetrieveVideoFileSerializer
from mession_square.serializers import TaskListSerializer

User = get_user_model()

class CreateVideoCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        parent_comment = None
        com_type = 1
        if attrs.get('parent_comment', ''):
            parent_comment = attrs['parent_comment']
        if attrs.get('com_type', ''):
            com_type = attrs['com_type']

        if (com_type != 1 or parent_comment != None):
            if com_type == 2:
                if False if parent_comment and parent_comment.com_type == 1 else True:
                    attrs['com_type'] = 1
            if parent_comment:
                if com_type == 1 or parent_comment.com_type != 1:
                    del attrs['parent_comment']
            else:
                attrs['com_type'] = 1
        return attrs

    class Meta:
        model = VideoComment
        fields = ['user', 'video', 'comment', 'com_type', 'parent_comment']


class RetieveVideoComment(serializers.ModelSerializer):
    user = UserProfileSerializer()

    def validate(self, attrs):
        id = attrs['id']
        user_id = attrs['user'].id
        try:
            user_point_love = UserPointLove.objects.get(video_comment_id=id, user_id=user_id)
            attrs['is_love'] = True
        except:
            pass
        return attrs

    class Meta:
        model = VideoComment
        fields = ['id', 'comment', 'add_time', 'user', 'point_love_nums', 'is_love']


class ListVideoCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    parent_com = RetieveVideoComment(many=True)

    def validate(self, attrs):
        id = attrs['id']
        user_id = attrs['user'].id
        try:
            user_point_love = UserPointLove.objects.get(video_comment_id=id, user_id=user_id)
            attrs['is_love'] = True
        except:
            pass
        return attrs

    class Meta:
        model = VideoComment
        fields = ['id', 'video', 'user', 'comment', 'parent_com', 'add_time', 'point_love_nums', 'is_love']


class UserPointLoveSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        reply_type = str(attrs['reply_type'])
        if reply_type == '1':
            if not VideoComment.objects.filter(id=int(attrs['video_comment'])):
                raise serializers.ValidationError("没有该条评论")
        else:
            if not VideoCommentReplyModel.objects.filter(id=int(attrs['video_comment'])):
                raise serializers.ValidationError("没有该条评论")
        return attrs

    class Meta:
        model = UserPointLove
        fields = ['id', 'user',  'video_comment', 'reply_type']
        validators = [
            UniqueTogetherValidator(
                queryset=UserPointLove.objects.all(),
                fields=('user', 'video_comment', 'reply_type'),
                message='已点赞'
            )
        ]


class UserFavDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    video = RetrieveVideoFileSerializer()

    class Meta:
        model = UserFavVideo
        fields = ['user', 'video']


class UserFavVideoSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFavVideo
        fields = ['user', 'video']
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavVideo.objects.all(),
                fields = ('user', 'video'),
                message='已收藏'
            )
        ]


class UserFavTaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFavMession
        fields = ['user', 'task']
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavMession.objects.all(),
                fields=('user', 'task'),
                message='已收藏'
            )
        ]


class UserFavTaskListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    task = TaskListSerializer()

    class Meta:
        model = UserFavMession
        fields = ['user', 'task', 'add_time']


class UserUploadFileSerializer(serializers.Serializer):
    texts = TextFileSerializer(many=True)


class TestComReplyListSerializer(serializers.ModelSerializer):
    from_uid = UserProfileSerializer()
    to_uid = UserProfileSerializer()

    class Meta:
        model = VideoCommentReplyModel
        fields = ['id', 'comment_id', 'reply_id', 'from_uid', 'to_uid', 'reply_type', 'comment', 'point_love_nums',
                  'is_love', 'add_time']


class TestVideoComListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    child_com = TestComReplyListSerializer(many=True)

    class Meta:
        model = VideoComment
        fields = ['id', 'user', 'video', 'comment', 'point_love_nums', 'is_love', 'add_time', 'child_com']


class TestComReplyCreateSerializer(serializers.ModelSerializer):
    from_uid = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_reply_id(self, reply_id):
        reply_type = str(self.initial_data['reply_type'])

        if reply_type == '1':
            reply_id = str(reply_id)
            comment_id = str(self.initial_data['comment_id'])
            print("reply_id", type(reply_id), "comment_id", type(comment_id))
            if reply_id != comment_id:
                raise serializers.ValidationError("没有该评论")
        else:
            if not VideoCommentReplyModel.objects.filter(id=reply_id, from_uid=self.initial_data['to_uid']):
                raise serializers.ValidationError("没有该评论")
        return reply_id

    class Meta:
        model = VideoCommentReplyModel
        fields = ['comment_id', 'reply_id', 'from_uid', 'to_uid', 'reply_type', 'comment',]


class TestVideoComCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    point_love_nums = serializers.IntegerField(read_only=True)
    is_love = serializers.BooleanField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VideoComment
        fields = ['user', 'video', 'comment', 'point_love_nums', 'is_love', 'add_time']