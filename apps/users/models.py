from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime
# Create your models here.


class UserProfile(AbstractUser):
    '''
    用户登录表
    '''
    PERSON_ID = (
        ('agri_owner', '农场主'),
        ('tea_owner', '专家'),
        ('student', '学生'),
    )
    row_id = models.CharField(choices=PERSON_ID,
                              default='student', max_length=15, verbose_name='用户身份', help_text='用户身份')
    mobile = models.CharField(max_length=11, verbose_name='手机号码', null=True, blank=True, help_text='手机号码(不填，后台处理)')
    is_del = models.BooleanField(default=False, verbose_name='是否删除', help_text='是否删除')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='字段添加时间', help_text='字段添加时间')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户登录'
        verbose_name_plural = verbose_name


class UserInfo(models.Model):
    '''
    用户个人信息表
    '''
    user = models.OneToOneField(UserProfile, related_name='user_profile', verbose_name='用户', help_text='用户')
    nick_name = models.CharField(max_length=20, default='', verbose_name='昵称', help_text='昵称')
    # image = models.ImageField(upload_to='user_img/%Y/%m/%d', default='user_img/default.png',
    #                           verbose_name='用户头像', help_text='用户头像')
    image = models.CharField(default="", max_length=81, verbose_name="七牛云上传图片地址", help_text="七牛云上传图片地址")
    birth = models.DateField(default=datetime.now, null=True, blank=True, help_text='用户生辰')
    sex = models.CharField(choices=(('male', '男'), ('female', '女')), default='female', max_length=7,
                           verbose_name='性别', help_text='性别')
    address = models.CharField(default='宇宙省地球市xxx街', null=True, blank=True, max_length=50, verbose_name='用户地址',
                               help_text='用户地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='字段添加时间', help_text='字段添加时间')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '用户个人信息表'
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    '''
    短信验证码
    '''
    code = models.CharField(max_length=10, verbose_name='验证码', help_text='验证码')
    mobile = models.CharField(max_length=11, verbose_name='手机号码', help_text='手机号码')
    code_type = models.CharField(max_length=15, choices=(('register', '注册'), ('reset_password', '忘记密码')),
                                 default='register', verbose_name='验证码类型', help_text='验证码类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='字段添加时间', help_text='字段添加时间')

    def __str__(self):
        return '{0}({1})'.format(self.mobile, self.code)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

