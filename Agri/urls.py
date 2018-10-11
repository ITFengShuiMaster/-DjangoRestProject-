"""Agricultural URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
#处理文件上传
from django.views.static import serve
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from Agri.settings import MEDIA_ROOT
from users.views import SemVerifyCodeSet, UserRegViewSet, PasswordResetViewSet, UserObtainJSONWebToken,\
    UserInfoUpdateViewSet, ZWP_UpdateUserInfoView
from courses.views import VideoFileViewSet, UploadVideoTokenView, VideoRecommendView
from operation.views import UserPointLoveViewSet, UserFavViewSet, UserUploadFileView, TestComAndReplyView,\
    TestReplyView
from mession_square.views import TaskViewSet, TaskReplyView, UserAttentionTaskView, TaskPointViewSet, \
    TaskReplyCommentViewSet, TaskReplyCommentReplyViewSet, WangEditerImageUploadView, LeaveMessageViewSet, \
    LeaveMessageReplyViewSet, MyTaskReplyViewSet, SnippetList
from resources.views import TextFileViewSet

import xadmin

router = DefaultRouter()

#用户发送验证码路由
router.register(r'code', SemVerifyCodeSet, base_name='code')
#用户注册, 查看个人信息， 更新个人信息路由
router.register(r'user', UserRegViewSet, base_name='register')
#更新个人信息路由
router.register(r're_user', UserInfoUpdateViewSet, base_name='re_user')
#忘记密码
router.register(r're_password', PasswordResetViewSet, base_name='re_password')
#视频列表
router.register(r'video', VideoFileViewSet, base_name='video')
#评论点赞
router.register(r'point', UserPointLoveViewSet, base_name='point')
#用户收藏视频
router.register(r'user_favs', UserFavViewSet, base_name='user_favs')
#用户上传文档
router.register(r'text', TextFileViewSet, base_name='text')
#用户显示上传文档
router.register(r'texts', UserUploadFileView, base_name='texts')
#用户评论
router.register('video_com', TestComAndReplyView, base_name='test_video_com')
#用户回复
router.register('video_reply', TestReplyView, base_name='test_video_reply')
#任务广场提问
router.register('task', TaskViewSet, base_name='task')
#任务广场回答
router.register('task_reply', TaskReplyView, base_name='task_reply')
#关注任务广场提问
router.register('task_fav', UserAttentionTaskView, base_name='task_fav')
#综合点赞
router.register("mession_point", TaskPointViewSet, base_name="mession_point")
#任务广场回答评论（主评论)
router.register("mession_com", TaskReplyCommentViewSet, base_name="mession_com")
#任务广场回答评论（子评论)
router.register("mession_reply", TaskReplyCommentReplyViewSet, base_name="mession_reply")
#任务广场：留言表功能
router.register("leave_message", LeaveMessageViewSet, base_name="leave_message")
#任务广场：留言表回复功能
router.register("leave_message", LeaveMessageViewSet, base_name="leave_message")
#任务广场：我的回答
router.register("my_reply", MyTaskReplyViewSet, base_name="my_reply")

router.register("reply_LM", LeaveMessageReplyViewSet, base_name="reply_LM")



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    #处理文件上传路由
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    #drfREST框架的登录和注销视图
    url(r'^api-auth/', include('rest_framework.urls')),
    #drf文档
    url(r'docs/', include_docs_urls(title="智慧农业综合产学研")),
    #jwt登录
    url(r'^login/$', obtain_jwt_token),

    #ViewSet路由
    url(r'^', include(router.urls)),

     #前端上传视频到七牛云，获得token
    url(r'^upload_video/$', UploadVideoTokenView.as_view(), name='test_video'),

    #登录测试
    url(r'^login_t/', UserObtainJSONWebToken.as_view()),

    #视频相关推荐
    url(r'^video_recommend/(?P<id>\d+)/$', VideoRecommendView.as_view(), name='video_recom'),

    #第三方登录
    url('', include('social_django.urls', namespace='social')),

    url('^test_weibo/$', TemplateView.as_view(template_name="test.html")),

    url('^image_upload/$', WangEditerImageUploadView.as_view(), name="image_upload"),

    url('^myReply/$', SnippetList.as_view(), name="myReply"),

]
