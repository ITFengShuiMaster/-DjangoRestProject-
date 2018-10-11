from django.db import models
from django.contrib.auth import get_user_model

from datetime import datetime

User = get_user_model()
# Create your models here.


class FileVideoModel(models.Model):
    user = models.ForeignKey(User, related_name='user_ptoi', verbose_name='上传视频用户', help_text='上传视频用户')
    video_name = models.CharField(max_length=11, verbose_name='视频名称', help_text='视频名称')
    desc = models.CharField(default='视频很好看，快来看吧!', max_length=41, verbose_name='视频描述', help_text='视频描述')
    # video_img = models.ImageField(upload_to='video_img/%Y/%m/%d', default='video_img/default.png', verbose_name='视频封面',
    #                               help_text='视频封面')
    video_img = models.CharField(default="http://p71yd5lgg.bkt.clouddn.com/default.png", max_length=81, verbose_name="七牛云视频封面", help_text="七牛云视频封面")
    click_num = models.IntegerField(default=0, verbose_name='视频点击量', help_text='视频点击量')
    fav_num = models.IntegerField(default=0, verbose_name='视频收藏量', help_text='视频收藏量')
    video_kind = models.CharField(choices=(('plant', '种植'),
                                           ('aquaculture', '水产养殖'),
                                           ('agri_industry', '农资业'),
                                           ('agri_and_sideline_industries', '农副加工业'),
                                           ('animal', '畜牧业')),
                                  default='plant',
                                  max_length=31,
                                  help_text='视频类别',
                                  verbose_name='视频类别')
    url = models.CharField(default="", max_length=200, help_text='访问地址', verbose_name="访问地址")
    video_file = models.FileField(default="", upload_to='video/%Y/%m', verbose_name='视频', help_text='视频')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='视频添加时间', help_text='视频添加时间')

    def __str__(self):
        return self.video_name

    class Meta:
        verbose_name = '视频资源'
        verbose_name_plural = verbose_name


class FileTestModel(models.Model):
    video_name = models.CharField(max_length=12, verbose_name='视频名称', help_text='视频名称')
    video = models.FileField(upload_to='video/%Y/%m', verbose_name='视频', help_text='视频')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='视频添加时间', help_text='视频添加时间')

    class Meta:
        verbose_name = '测试视频上传'
        verbose_name_plural = verbose_name