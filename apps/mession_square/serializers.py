# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/5/15 16:19'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import TaskModel, TaskReplyModel, UserAttentionTask, TaskPointModel, TaskReplyComment,\
    TaskReplyCommentReplyModel, LeaveMessageModel, LeaveMessageReplyModel
from users.serializers import UserProfileSerializer


class TaskCreateSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate_mession_kind(self, mession_kind):
        a = 1
        res = mession_kind.replace('[', '').replace(']', '').split(",")
        res = '、'.join(res)
        return res

    def validate(self, attrs):
        level_task = {
            'agri_owner': 3,
            'tea_owner': 3,
            'student': 2,
        }

        rowIstr = self.context['request'].user.row_id
        attrs['task_level'] = level_task[rowIstr]
        return attrs

    class Meta:
        model = TaskModel
        fields = ['user', 'title', 'content', 'mession_kind',]
        validators = [
            UniqueTogetherValidator(
                queryset=TaskModel.objects.all(),
                fields=('user', 'title'),
                message="该问题已经提问过了!",
            )
        ]


class TaskReplyCreateSearializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TaskReplyModel
        fields = ['user', 'task', 'content']


class TaskReplyListSearializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = TaskReplyModel
        fields = ['id', 'user', 'task', 'content', 'point_nums', 'comment_nums', 'add_times']


class TaskListAndRetrieveSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    # task_reply = TaskReplyListSearializer(many=True)

    class Meta:
        model = TaskModel
        fields = ['id', 'user', 'title', 'content', 'mession_kind', 'attention_nums', 'reply_nums', 'add_times']


class TaskListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = TaskModel
        fields = ['user', 'title', 'content', 'mession_kind', 'point_nums', 'attention_nums', 'add_times']


class UserAttentionTaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAttentionTask
        fields = ['user', 'task']
        validators = [
            UniqueTogetherValidator(
                queryset=UserAttentionTask.objects.all(),
                fields=('user', 'task'),
                message='已关注'
            )
        ]


class UserAttentionTaskListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    task = TaskListAndRetrieveSerializer()

    class Meta:
        model = UserAttentionTask
        fields = ['user', 'task', 'add_times']


class TaskPointSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        return attrs

    class Meta:
        model = TaskPointModel
        fields = ['user', 'to_id', 'to_id_type']
        validators = [
            UniqueTogetherValidator(
                queryset=TaskPointModel.objects.all(),
                fields=('user', 'to_id', 'to_id_type'),
                message='已点赞'
            )
        ]


class TaskReplyCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = TaskReplyComment
        fields = ['user', 'task_reply', 'comment']


class TaskReplyCommentListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = TaskReplyComment
        fields = ['id', 'user', 'task_reply', 'comment', 'point_nums', 'is_love', 'add_time']


class TaskReplyCommentReplyCreateSerializer(serializers.ModelSerializer):
    from_uid = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        reply_type = attrs['reply_type']
        reply_id = attrs['reply_id']
        to_uid = attrs['to_uid']
        comment_id = attrs['comment_id']

        if reply_type == 1:
            if reply_id != comment_id.id:
                raise serializers.ValidationError("reply_id 和 comment_id不一致")
            if not TaskReplyComment.objects.filter(id=reply_id, user=to_uid):
                raise serializers.ValidationError("不存在该条评论")
        else:
            if not TaskReplyCommentReplyModel.objects.filter(comment_id=comment_id, from_uid=to_uid, id=reply_id):
                raise serializers.ValidationError("不存在该条评论")
        return attrs

    class Meta:
        model = TaskReplyCommentReplyModel
        fields = ['comment_id', 'reply_id', 'from_uid', 'to_uid', 'reply_type', 'comment']


class TaskReplyCommentReplyListSerializer(serializers.ModelSerializer):
    from_uid = UserProfileSerializer()
    to_uid = UserProfileSerializer()

    class Meta:
        model = TaskReplyCommentReplyModel
        fields = ['id', 'from_uid', 'to_uid', 'comment', 'point_nums', 'add_time']


class LeaveMessageCreateSerializer(serializers.ModelSerializer):

    def validate_receive_user(self, receive_user):
        a = 1
        if receive_user.row_id != "tea_owner":
            raise serializers.ValidationError("该用户不是专家")
        return receive_user

    class Meta:
        model = LeaveMessageModel
        fields = ['send_user', 'receive_user', "content"]


class LeaveMessageReplyListSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = LeaveMessageReplyModel
        fields = ['user', 'leaveM', 'content', 'add_time']


class LeaveMessageListSerializer(serializers.ModelSerializer):
    send_user = UserProfileSerializer()
    leaveM_Reply = LeaveMessageReplyListSerializer(many=True)

    class Meta:
        model = LeaveMessageModel
        fields = ['send_user', 'receive_user', "content", "leaveM_Reply", "add_time"]


class LeaveMessageReplyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveMessageReplyModel
        fields = ['user', 'leaveM', 'content']


class MyTaskReplyListSearializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    task = TaskListAndRetrieveSerializer()

    class Meta:
        model = TaskReplyModel
        fields = ['id', 'user', 'task', 'content', 'point_nums', 'comment_nums', 'add_times']


class MyTaskListAndRetrieveSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer()
    task_reply = TaskReplyListSearializer(many=True)

    class Meta:
        model = TaskModel
        fields = ['id', 'user', 'title', 'content', 'mession_kind', 'attention_nums', 'reply_nums', 'task_reply', 'add_times']