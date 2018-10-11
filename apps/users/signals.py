# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/12 19:50'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import UserInfo

import datetime

User = get_user_model()

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        user_info = UserInfo(user=instance, nick_name=instance.mobile if instance.mobile else instance.username, image='http://p71yd5lgg.bkt.clouddn.com/default.png',
                             birth=datetime.datetime.now(), sex='female', address='宇宙省地球市xxx街')
        if instance.is_superuser:
            user_info.save()
            return
        instance.set_password(instance.password)
        instance.save()
        user_info.save()