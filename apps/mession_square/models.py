from django.db import models
from django.contrib.auth import get_user_model

from DjangoUeditor.models import UEditorField

from datetime import datetime
User = get_user_model()
# Create your models here.


class TaskModel(models.Model):
    TASK_LEVEL = (
        (1, '游客级别'),
        (2, '普通用户界别'),
        (3, '教师级别'),
    )

    user = models.ForeignKey(User, related_name='task_user', verbose_name="提问用户", help_text='提问用户')
    title = models.CharField(max_length=25, verbose_name='提问标题', help_text='提问标题')
    content = models.TextField(verbose_name="问题内容", help_text="问题内容")
    mession_kind = models.CharField(max_length=36, verbose_name="问题分类", help_text="问题分类")
    attention_nums = models.IntegerField(default=0, verbose_name="关注数", help_text="关注数")
    reply_nums = models.IntegerField(default=0, verbose_name="回答数", help_text="回答数")
    task_level = models.IntegerField(default=1, choices=TASK_LEVEL, verbose_name="问题级别", help_text="问题级别")

    add_times = models.DateField(default=datetime.now, verbose_name="创建时间", help_text="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "提问表"
        verbose_name_plural = verbose_name


class UserAttentionTask(models.Model):
    user = models.ForeignKey(User, verbose_name="关注用户", help_text="关注用户")
    task = models.ForeignKey(TaskModel, verbose_name="关注问题", help_text="关注的问题")
    add_times = models.DateField(default=datetime.now, verbose_name="创建时间", help_text="创建时间")

    def __str__(self):
        return self.task.title

    class Meta:
        verbose_name = "关注表"
        verbose_name_plural = verbose_name


class TaskReplyModel(models.Model):
    user = models.ForeignKey(User, related_name='task_reply_user', verbose_name='回答用户', help_text='回答用户')
    task = models.ForeignKey(TaskModel, related_name="task_reply", verbose_name="回答的问题", help_text="回答的问题")
    content = models.TextField(verbose_name="回答内容", help_text="回答内容")
    point_nums = models.IntegerField(default=0, verbose_name="点赞数", help_text="点赞数")
    is_love = models.BooleanField(default=False, verbose_name="是否点赞", help_text="是否点赞")
    comment_nums = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    add_times = models.DateField(default=datetime.now, verbose_name="创建时间", help_text="创建时间")

    def __str__(self):
        return self.content[:21]

    class Meta:
        verbose_name = "回答表"
        verbose_name_plural = verbose_name


class TaskReplyComment(models.Model):

    user = models.ForeignKey(User, verbose_name='评论用户', help_text='评论用户')
    task_reply = models.ForeignKey(TaskReplyModel, verbose_name='所评论的回答',
                              help_text='所评论的回答')
    comment = models.CharField(max_length=150, verbose_name='评论内容', help_text='评论内容')
    point_nums = models.IntegerField(default=0, verbose_name='点赞数', help_text='点赞数')
    comment_nums = models.IntegerField(default=0, verbose_name="评论数", help_text="评论数")
    is_love = models.BooleanField(default=False, verbose_name='是否点过赞', help_text='是否点过赞')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '{0}'.format(self.comment[:21])

    class Meta:
        verbose_name = '二级评论表'
        verbose_name_plural = verbose_name


class TaskReplyCommentReplyModel(models.Model):
    REPLY_TYPE = (
        (1, '回复主评论的回复'),
        (2, '回复的回复'),
    )

    comment_id = models.ForeignKey(TaskReplyComment, null=True, on_delete=models.SET_NULL, verbose_name='根评论', help_text='根评论')
    reply_id = models.IntegerField(verbose_name='回复目标id', help_text='回复目标id')
    from_uid = models.ForeignKey(User, related_name="task_reply_from_uid", verbose_name='回复用户', help_text='回复用户')
    to_uid = models.ForeignKey(User, related_name="task_reply_to_uid", verbose_name='目标用户id', help_text='目标用户id')
    reply_type = models.IntegerField(default=1, choices=REPLY_TYPE, verbose_name='回复类型',
                                     help_text="(1, '回复主评论的回复'),(2, '回复子评论的回复'),")
    comment = models.CharField(max_length=150, verbose_name='评论内容', help_text='评论内容')
    point_nums = models.IntegerField(default=0, verbose_name='点赞数', help_text='点赞数')
    is_love = models.BooleanField(default=False, verbose_name='是否点过赞', help_text='是否点过赞')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '{0}'.format(self.comment_id)

    class Meta:
        verbose_name = '二级回复表'
        verbose_name_plural = verbose_name


class TaskPointModel(models.Model):
    TYPES = (
        (1, "点赞回答"),
        (2, "点赞根评论"),
        (3, "点赞子评论"),
    )
    user = models.ForeignKey(User, verbose_name="点赞_用户", help_text="点赞_用户")
    to_id = models.IntegerField(default=1, verbose_name="目标id", help_text="目标id")
    to_id_type = models.IntegerField(default=1, choices=TYPES, verbose_name="点赞类型", help_text="点赞类型:1(点赞回答)，2(点赞根评论)，3(点赞子评论)")
    add_times = models.DateField(default=datetime.now, verbose_name="创建时间", help_text="创建时间")

    def __str__(self):
        return self.to_id_type

    class Meta:
        verbose_name = "点赞表"
        verbose_name_plural = verbose_name


class LeaveMessageModel(models.Model):
    send_user = models.ForeignKey(User, related_name="L_M_send_user", verbose_name="发送人", help_text="发送人id")
    receive_user = models.ForeignKey(User, related_name="L_M_receive_user", verbose_name="接收人", help_text="接收人id")
    content = models.CharField(max_length=199, verbose_name="回复内容", help_text="回复内容")
    add_time = models.DateField(default=datetime.now, verbose_name="留言时间")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "留言表"
        verbose_name_plural = verbose_name


class LeaveMessageReplyModel(models.Model):
    user = models.ForeignKey(User, verbose_name="回复人", help_text="回复人id")
    leaveM = models.ForeignKey(LeaveMessageModel, related_name="leaveM_Reply", verbose_name="留言表", help_text="留言表id")
    content = models.CharField(max_length=199, verbose_name="回复内容", help_text="回复内容")
    add_time = models.DateField(default=datetime.now, verbose_name="回复时间")

