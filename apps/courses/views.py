from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from django_filters.rest_framework import DjangoFilterBackend
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse

from .models import FileVideoModel
from .serializers import ListVideoFileSerializer, RetrieveVideoFileSerializer, CreateVideoFileSerializer
from utils.permissions import IsTeacherPermision
from utils.qi_niu_upload import return_token, upload_video
from Agri.settings import BASE_DIR

import os
import threading
# Create your views here.


class VideoPagination(pagination.PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'


class Upload_Video_Thread (threading.Thread):
    def __init__(self, video_file_url, video):
        threading.Thread.__init__(self)
        self.video_file_url = video_file_url
        self.video = video

    def run(self):
        from Agri.settings import WL
        key = upload_video(self.video_file_url)
        self.video.url = "http://p71yd5lgg.bkt.clouddn.com/" + key
        self.video.save()


class VideoFileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    视屏接口
    list:
    视频列表页
    retrieve:
    视频详情页
    create:
    上传视屏页， 其中只有专家可以上传视屏
    '''
    queryset = FileVideoModel.objects.all()
    pagination_class = VideoPagination
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RetrieveVideoFileSerializer
        elif self.action == 'create':
            return CreateVideoFileSerializer
        return ListVideoFileSerializer

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticatedOrReadOnly(), ]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsTeacherPermision()]
        return []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('video_kind',)
    search_fields = ('video_name', 'desc', 'user__user_profile__nick_name')
    ordering_fields = ('add_time', 'click_num')


class VideoRecommendView(APIView):
    '''
        视频相关推荐
        id 为视频id
    '''

    def get(self, request, id, format=None):
        try:
            instance = FileVideoModel.objects.get(id=id)
            snippets = FileVideoModel.objects.filter(video_kind=instance.video_kind).order_by('-click_num')
            serializer = ListVideoFileSerializer(snippets, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "不存在该id"})

    def post(self, request, format=None):
        serializer = ListVideoFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadVideoTokenView(View):
    def get(self, request):
        from random import randint
        import json
        token = return_token()

        return HttpResponse(json.dumps({"token": token}), content_type='application/json')

    def post(self, request):
        a = 1
        print(a)
        return "hello"

