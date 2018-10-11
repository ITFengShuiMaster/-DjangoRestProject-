from django.db import models

from datetime import datetime

from users.models import UserProfile
from courses.models import FileVideoModel
from resources.models import TextModel
from mession_square.models import TaskModel
# Create your models here.


class VideoComment(models.Model):

    user = models.ForeignKey(UserProfile, related_name='test_video_user_comment', verbose_name='评论用户', help_text='评论用户')
    video = models.ForeignKey(FileVideoModel, related_name='test_video_file_comment', verbose_name='所评论的视频',
                              help_text='所评论的视频')
    comment = models.CharField(max_length=150, verbose_name='评论内容', help_text='评论内容')
    point_love_nums = models.IntegerField(default=0, verbose_name='点赞数', help_text='点赞数')
    is_love = models.BooleanField(default=False, verbose_name='是否点过赞', help_text='是否点过赞')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '{0}:{1}'.format(self.video.video_name, self.comment[:20])

    class Meta:
        verbose_name = '二级评论表'
        verbose_name_plural = verbose_name


class VideoCommentReplyModel(models.Model):
    REPLY_TYPE = (
        (1, '回复评论的回复'),
        (2, '回复的回复'),
    )

    comment_id = models.ForeignKey(VideoComment, null=True, on_delete=models.SET_NULL, related_name='child_com', verbose_name='根评论', help_text='根评论')
    reply_id = models.IntegerField(verbose_name='回复目标id', help_text='回复目标id')
    from_uid = models.ForeignKey(UserProfile, related_name='test_reply_user_from_uid', verbose_name='回复用户', help_text='回复用户')
    to_uid = models.ForeignKey(UserProfile, related_name='test_reply_user_to_uid', verbose_name='目标用户id', help_text='目标用户id')
    reply_type = models.IntegerField(default=1, choices=REPLY_TYPE, verbose_name='回复类型', help_text='回复类型')
    comment = models.CharField(max_length=150, verbose_name='评论内容', help_text='评论内容')
    point_love_nums = models.IntegerField(default=0, verbose_name='点赞数', help_text='点赞数')
    is_love = models.BooleanField(default=False, verbose_name='是否点过赞', help_text='是否点过赞')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '{0}:{1}'.format(self.comment_id, self.comment[:20])

    class Meta:
        verbose_name = '二级回复表'
        verbose_name_plural = verbose_name


class UserPointLove(models.Model):
    REPLY_TYPE = (
        (1, '回复评论的回复'),
        (2, '回复的回复')
    )

    user = models.ForeignKey(UserProfile, related_name='user_point', verbose_name='用户', help_text='用户')
    video_comment = models.IntegerField(verbose_name='评论', help_text='评论id')
    reply_type = models.IntegerField(choices=REPLY_TYPE, verbose_name='点赞类型', help_text='点赞类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '{0}-{1}'.format(self.user.username, self.video_comment)

    class Meta:
        verbose_name = '用户点赞'
        verbose_name_plural = verbose_name


class UserFavVideo(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='收藏用户', help_text='收藏用户')
    video = models.ForeignKey(FileVideoModel, related_name='file_video', verbose_name='收藏的视屏', help_text='收藏视频')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '收藏用户:{0}\n收藏视频:{1}'.format(self.user.username, self.video.video_name)

    class Meta:
        verbose_name = '视频收藏'
        verbose_name_plural = verbose_name


class UserFavMession(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='收藏用户', help_text='收藏用户')
    task = models.ForeignKey(TaskModel, verbose_name="收藏问答", help_text="收藏问答")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return '收藏用户:{0}\n收藏问答:{1}'.format(self.user.username, self.task.title)

    class Meta:
        verbose_name = '问答收藏'
        verbose_name_plural = verbose_name


class UserUploadFile(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='上传用户', help_text='上传用户')
    text = models.ForeignKey(TextModel, related_name='texts', verbose_name='上传文档', help_text='上传文档')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户上传文档'
        verbose_name_plural = verbose_name

