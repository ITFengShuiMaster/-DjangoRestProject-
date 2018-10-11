from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import UserPointLove, UserFavVideo, UserUploadFile, VideoComment, VideoCommentReplyModel, UserFavMession
from .serializers import ListVideoCommentSerializer, CreateVideoCommentSerializer,\
    UserPointLoveSerializer, UserFavVideoSerializer, UserFavDetailSerializer, UserUploadFileSerializer,\
    TestVideoComListSerializer, TestComReplyListSerializer, TestVideoComCreateSerializer, TestComReplyCreateSerializer,\
    UserFavTaskSerializer, UserFavTaskListSerializer
from utils.permissions import IsOwerPermision, IsSuperPermision

import os
# Create your views here.


class VideoComPagination(pagination.PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'


class UserPointLoveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
        评论点赞功能
        create:
            因为表中是联合查询（user+video_comment)，需要评论的id
            reply_type是点赞评论的类型，1：代表主评论, 2：代表子评论
        retrieve:
            测试需要，不用参考
        destroy:
            需要的是评论id, 并且在body体中传入reply_type(
                                                reply_type:1---表示主评论
                                                reply_type:2---表示子评论
            )
    '''
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, IsOwerPermision)
    serializer_class = UserPointLoveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        reply_type = str(request.data['reply_type'])
        video_comment_id = request.data['video_comment']

        if reply_type == '1':
            if not VideoComment.objects.filter(id=int(video_comment_id)):
                return Response({"detail": "没有该条评论"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if not VideoCommentReplyModel.objects.filter(id=int(video_comment_id)):
                return Response({"detail": "没有该条评论"}, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        if request.data['reply_type']:
            reply_type_id = request.data['reply_type']
        else:
            return Response({"detail": "请求体中需要reply_type"}, status=status.HTTP_400_BAD_REQUEST)
        instance = None
        if reply_type_id == '1':
            if not UserPointLove.objects.filter(video_comment=int(kwargs['pk']), reply_type=1, user=request.user):
                return Response({"detail": "该条评论未点赞"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance = UserPointLove.objects.filter(video_comment=int(kwargs['pk']), reply_type=1, user=request.user)
        else:
            if not UserPointLove.objects.filter(video_comment=int(kwargs['pk']), reply_type=2, user=request.user):
                return Response({"detail": "该条评论未点赞"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                instance = UserPointLove.objects.filter(video_comment=int(kwargs['pk']), reply_type=2, user=request.user)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return UserPointLove.objects.filter(user=self.request.user)


class UserFavViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, IsOwerPermision)
    lookup_field = 'video_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return UserFavDetailSerializer
        return UserFavVideoSerializer

    def get_queryset(self):
        return UserFavVideo.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = UserFavVideo.objects.get(video_id=kwargs['video_id'], user=request.user)
            return Response({"video": instance.video_id})
        except:
            return Response({"video": "null"})


class UserFavTaskView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = UserFavMession.objects.all()
    authentication = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == 'create':
            return UserFavTaskSerializer
        return UserFavTaskListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAuthenticated(), IsOwerPermision()]


class UserUploadFileView(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = UserUploadFileSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return UserUploadFile.objects.filter(user=self.request.user)


class TestComAndReplyView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
        二级评论接口
        list:
            测试用
        retrieve:
            id 是视频id
        create:
            创建评论,乃根评论
        destroy:
            id 是根评论的id, 级联删除， 只有超级管理员可以删除评论
    '''
    queryset = VideoComment.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = VideoComPagination
    permission_classes = (permissions.IsAuthenticated,)
    # lookup_field = 'video_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return TestVideoComCreateSerializer
        return TestVideoComListSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list' or self.action == 'retrieve':
            return [permissions.IsAuthenticated(),]
        return [permissions.IsAuthenticated(), IsSuperPermision()]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        re_data = serializer.data
        for index, data in enumerate(re_data):
            data['add_time'] = data['add_time'].replace("T", " ")
            if data['child_com']:
                child_re_data = data['child_com']
                for index, child_data in enumerate(child_re_data):
                    child_data['add_time'] = child_data['add_time'].replace("T", " ")
                    child_re_data[index] = child_data
                data['child_com'] = child_re_data
            re_data[index] = data
        return Response(re_data)

    def filter_is_love(self, request, re_data):
        for index, data in enumerate(re_data):
            if UserPointLove.objects.filter(user=request.user, video_comment=data['id'], reply_type=1):
                data['is_love'] = True
            data['add_time'] = data['add_time'].replace("T", " ")

            if data['child_com']:
                for index_child, child_data in enumerate(data['child_com']):
                    if UserPointLove.objects.filter(user=request.user, video_comment=child_data['id'],
                                                    reply_type=2).order_by('-add_time'):
                        child_data['is_love'] = True
                    child_data['add_time'] = child_data['add_time'].replace("T", " ")
                    data['child_com'][index_child] = child_data

            re_data[index] = data
        return re_data

    def retrieve(self, request, *args, **kwargs):
        instance = VideoComment.objects.filter(video_id=kwargs['pk']).order_by('-add_time')
        serializer = self.get_serializer(instance, many=True)
        re_data = self.filter_is_love(request, serializer.data)

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            re_data = self.filter_is_love(request, serializer.data)
            return self.get_paginated_response(re_data)

        return Response(re_data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        destroy_reply = VideoCommentReplyModel.objects.filter(comment_id=instance.id)
        destroy_reply.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TestReplyView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
        二级回复表
        list：
            测试用
        create:
            创建回复
        destroy:
            删除回复,id为回复的id
    '''
    queryset = VideoCommentReplyModel.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'create':
            return TestComReplyCreateSerializer
        return TestComReplyListSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            return [permissions.IsAuthenticated(),]
        return [permissions.IsAuthenticated(), IsSuperPermision()]