# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/25 15:04'

#独立使用django model
import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Agri.settings")


import django
django.setup()

from courses.models import FileVideoModel

VIDEO_KIND = ['plant', 'agri_and_sideline_industries', 'agri_industry', 'aquaculture', 'animal']
VIDEO_IMG = [
            'http://p71yd5lgg.bkt.clouddn.com/%E6%B4%8B%E8%91%B1.jpg',
             'http://p71yd5lgg.bkt.clouddn.com/%E5%9C%9F%E8%B1%86.jpg',
             'http://p71yd5lgg.bkt.clouddn.com/%E8%8A%B9%E8%8F%9C.jpg',
             'http://p71yd5lgg.bkt.clouddn.com/%E8%9E%83%E8%9F%B9.jpg',
             'http://p71yd5lgg.bkt.clouddn.com/%E5%8D%97%E7%93%9C.jpg'
             ]
VIDEO_USER = [16, 17, 18, 19, 20]

# for index in range(1, 101):
#     video = FileVideoModel()
#     video.video_name = 'test' + str(index)
#     video.desc = 'xxxx'
#     video.qi_niu_video_img = VIDEO_IMG[index%5]
#     video.click_num = 0
#     video.fav_num = 0
#     video.video_kind = VIDEO_KIND[index%5]
#     video.url = 'http://p71yd5lgg.bkt.clouddn.com/test1.mp4'
#     video.user_id = VIDEO_USER[index%5]
#     video.save()

count = 1
for video in FileVideoModel.objects.filter(video_name__contains="test"):
    video.video_img = VIDEO_IMG[count%5]
    video.save()
    count += 1
