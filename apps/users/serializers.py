# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/8 16:44'

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

from .models import VerifyCode, UserInfo
from Agri.settings import REGEX_MOBILE

from datetime import datetime
from datetime import timedelta

User = get_user_model()


class SemVerifycodeSerializers(serializers.Serializer):
    mobile = serializers.CharField(max_length=11, min_length=11, required=True,
                                   error_messages={
                                       'required': '请填写手机号',
                                       'blank': '请填写手机号',
                                       'max_length': '手机号码格式不正确',
                                       'min_length': '手机号码格式不正确',
                                   })
    code_type = serializers.CharField(max_length=15, required=True, help_text='验证码类型(register:注册, reset_password:忘记密码)',
                                      error_messages={
                                          'required': '请填写验证码类型',
                                          'blank': '请填写验证码类型',
                                          'max_length': '验证码类型不正确',
                                      })

    def validate_code_type(self, code_type):
        if not (code_type == 'register' or code_type == 'reset_password'):
            raise serializers.ValidationError("验证码类型错误")
        return code_type

    def validate_mobile(self, mobile):
        '''
        手机号验证
        :param mobile:
        :return:
        '''
        #验证手机号码是否合法
        import re
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码格式不正确")
        #验证操作是否超过一分钟
        one_minute = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if self.initial_data['code_type'] == 'register':
            # 验证手机号码是否存在
            if User.objects.filter(mobile=mobile).count():
                raise serializers.ValidationError("手机号码已注册")
            if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute, code_type='register'):
                raise serializers.ValidationError("操作时间未超过一分钟")
        else:
            # 验证手机号码是否存在
            if not User.objects.filter(mobile=mobile).count():
                raise serializers.ValidationError("手机号码未注册")
            if VerifyCode.objects.filter(mobile=mobile, add_time__gt=one_minute, code_type='reset_password'):
                raise serializers.ValidationError("操作时间未超过一分钟")
        return mobile


class UserInfoSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(default='user_img/default.png', max_length=21, help_text='头像', required=False)
    birth = serializers.DateField(format="%Y-%m-%d", required=False)

    class Meta:
        model = UserInfo
        fields = ['image', 'birth', 'sex', 'address', 'nick_name']


class ZWP_UserInfoSerializer(serializers.ModelSerializer):
    # image = serializers.ImageField(default='user_img/default.png', max_length=21, help_text='头像', required=False)
    # birth = serializers.DateField(format="%Y-%m-%d", required=False)

    class Meta:
        model = UserInfo
        fields = ['image', 'birth', 'sex', 'address', 'nick_name']


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    birth = serializers.DateField(format="%Y-%m-%d", required=False)

    class Meta:
        model = UserInfo
        fields = ['image', 'birth', 'sex', 'address', 'nick_name']


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, required=True,write_only=True,help_text='验证码',
                                 error_messages={
                                     'required': '请填写验证码',
                                     'blank': '请填写验证码',
                                     'max_length': '验证码格式不正确',
                                     'min_length': '验证码格式不正确',
                                 })
    username = serializers.CharField(required=True, allow_blank=False, max_length=11, min_length=11,help_text='手机号',
                                     validators=[UniqueValidator(queryset=User.objects.all(), message='手机号码已注册')],
                                     error_messages={
                                        'required': '请填写手机号',
                                        'blank': '请填写手机号',
                                        'max_length': '手机号码格式不正确',
                                        'min_length': '手机号码格式不正确',
                                     })
    password = serializers.CharField(required=True, allow_blank=False, min_length=6,
                                     style={'input_type': 'password'}, write_only=True,
                                     error_messages={
                                         'required': '请填写密码',
                                         'blank': '请填写密码',
                                         'min_length': '密码最小6位',
                                     })

    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    def validate_code(self, code):
        codes = VerifyCode.objects.filter(code=code, mobile=self.initial_data['username'], code_type='register').order_by('-add_time')
        if codes:
            verify_code = codes[0]
            two_minutes = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
            if verify_code.add_time < two_minutes:
                raise serializers.ValidationError("验证码已过期")
            if verify_code.code != code:
                raise serializers.ValidationError("验证码不正确")
        else:
            raise serializers.ValidationError("验证码不正确")

    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']
        return attrs

    class Meta:
        model = User
        fields = ['username', 'password', 'mobile', 'code',]


class UserProfileSerializer(serializers.ModelSerializer):
    user_profile = UserInfoSerializer()
    mobile = serializers.CharField(read_only=True)
    row_id = serializers.CharField(read_only=True)

    def validate_user_profile(self, user_profile):
        a = 1
        return user_profile

    def update(self, instance, validated_data):
        instance.user_profile.image = validated_data['user_profile']['image']
        instance.user_profile.nick_name = validated_data['user_profile']['nick_name']
        instance.user_profile.birth = validated_data['user_profile']['birth']
        instance.user_profile.sex = validated_data['user_profile']['sex']
        instance.user_profile.address = validated_data['user_profile']['address']
        instance.user_profile.save()

        return instance

    class Meta:
        model = User
        fields = ['id', 'mobile', 'row_id', 'user_profile']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    user_profile = UserInfoUpdateSerializer()
    mobile = serializers.CharField(read_only=True)
    row_id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'mobile', 'row_id', 'user_profile']


class PasswordResetSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, allow_blank=False, max_length=11, min_length=11,help_text='手机号码',
                                     error_messages={
                                         'required': '请填写手机号',
                                         'blank': '请填写手机号',
                                         'max_length': '手机号码格式不正确',
                                         'min_length': '手机号码格式不正确',
                                     })
    code = serializers.CharField(max_length=4, min_length=4, required=True, allow_blank=False, write_only=True,help_text='验证码',
                                 error_messages={
                                     'required': '请填写验证码',
                                     'blank': '请填写验证码',
                                     'max_length': '验证码格式不正确',
                                     'min_length': '验证码格式不正确',
                                 })
    password = serializers.CharField(required=True, allow_blank=False, min_length=6,write_only=True,
                                     error_messages={
                                         'required': '请填写密码',
                                         'blank': '请填写密码',
                                         'min_length': '密码最小六位',
                                     })
    password1 = serializers.CharField(required=True, allow_blank=False, min_length=6,write_only=True,
                                         error_messages={
                                             'required': '请填写密码',
                                             'blank': '请填写密码',
                                             'min_length': '密码最小六位',
                                         })

    def validate_username(self, username):
        user_cords = User.objects.filter(username=username)
        if not user_cords:
            raise serializers.ValidationError("手机号码未注册")
        return username

    def validate_code(self, code):
        re_cords = VerifyCode.objects.filter(mobile=self.initial_data['username'], code=code, code_type='reset_password').order_by('-add_time')
        if re_cords:
            last_code = re_cords[0]
            two_minutes = datetime.now() - timedelta(hours=0, minutes=2, seconds=0)
            if last_code.add_time < two_minutes:
                raise serializers.ValidationError("验证码已过期")
            if last_code.code != code:
                raise serializers.ValidationError("验证码不正确")
        else:
            raise serializers.ValidationError("验证码不正确")

    def validate(self, attrs):
        password1 = attrs['password']
        password2 = attrs['password1']
        if password1 != password2:
            raise serializers.ValidationError("密码不一致")
        del attrs['password1']
        del attrs['code']
        return attrs

    def update(self, instance, validated_data):
        user = super(PasswordResetSerializer, self).update(instance=instance, validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'code', 'password', 'password1']


class TestImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=21)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    birth = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = UserInfo
        fields = ['user', 'image', 'birth']




