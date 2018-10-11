from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import authentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.views import APIView

from django.views.generic.base import View
from django.http import HttpResponse

from .models import TaskModel, TaskReplyModel, UserAttentionTask, TaskPointModel, TaskReplyComment,\
    TaskReplyCommentReplyModel, LeaveMessageModel, LeaveMessageReplyModel
from .serializers import TaskCreateSerializers, TaskListAndRetrieveSerializer, TaskReplyCreateSearializer, \
    UserAttentionTaskSerializer, TaskReplyListSearializer, TaskPointSerializer, TaskReplyCommentCreateSerializer, \
    TaskReplyCommentListSerializer, TaskReplyCommentReplyCreateSerializer, TaskReplyCommentReplyListSerializer, \
    LeaveMessageCreateSerializer, LeaveMessageListSerializer, LeaveMessageReplyCreateSerializer, \
    LeaveMessageReplyListSerializer, MyTaskReplyListSearializer, MyTaskListAndRetrieveSerializer, \
    UserAttentionTaskListSerializer
from utils.permissions import IsOwerPermision, UserInfoOwerPermision, LeaveMessageOwerPermision, \
    LeaveMessageReplyOwerPermision
from Agri.settings import MEDIA_ROOT


class TaskPaginationClass(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'


class TaskViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
        任务广场
        list:
            显示所有问题
        create:
            创建问题
        retrieve:
            问题的详细信息
    '''
    queryset = TaskModel.objects.all().order_by('-task_level')
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('mession_kind', 'task_reply__user')
    search_fields = ('title', 'content')
    ordering_fields = ('add_times', 'attention_nums', 'reply_nums', 'task_level')
    pagination_class = TaskPaginationClass

    def get_permissions(self):
        # if self.action == "list" or self.action == "retrieve":
        #     return []
        return [permissions.IsAuthenticated(),]

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return TaskListAndRetrieveSerializer
        return TaskCreateSerializers

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            re_data = serializer.data
            for index, data in enumerate(re_data):
                if UserAttentionTask.objects.filter(user=request.user, task=int(data['id'])):
                    data['is_atn'] = True
                else:
                    data['is_atn'] = False
                re_data[index] = data

            return self.get_paginated_response(re_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TaskReplyView(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
        任务广场回答
        list:
        测试用
        retrieve:
        指定问题id获取所有回答
        create:
        创建回答

    '''
    queryset = TaskReplyModel.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = TaskPaginationClass

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return TaskReplyListSearializer
        return TaskReplyCreateSearializer

    def get_permissions(self):
        if self.action == 'list':
            return []
        return [permissions.IsAuthenticated(), ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = TaskReplyModel.objects.filter(task=kwargs['pk'])
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            re_data = serializer.data
            for index,data in enumerate(re_data):
                if TaskPointModel.objects.filter(user=request.user, to_id=data['id'], to_id_type=1):
                    data['is_love'] = True
                else:
                    data['is_love'] = False
                re_data[index] = data
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class UserAttentionTaskView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    任务广场：关注问题
    list:
        测试用
    create:
        关注某一个问题
    destroy:
        删除关注，指定问题的id
    '''
    queryset = UserAttentionTask.objects.all()
    # serializer_class = UserAttentionTaskSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwerPermision)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_serializer_class(self):
        if self.action == "list":
            return UserAttentionTaskListSerializer
        return UserAttentionTaskSerializer

    def get_queryset(self):
        return UserAttentionTask.objects.filter(user=self.request.user)

    def get_object(self, task_id):
        try:
            return UserAttentionTask.objects.get(user=self.request.user, task=task_id)
        except:
            return Response({"error":"没有关注该问题"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(task_id=kwargs['pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class TaskPointViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
        任务广场：综合点赞（点赞升级版）
        list:
            测试用
        delete:
            在请求体中标明删除的点赞类型to_id_type：   (1, "点赞回答"),
                                            (2, "点赞根评论"),
                                            (3, "点赞子评论"),
        create:
            指明点赞类型to_id_type：   (1, "点赞回答"),
                                            (2, "点赞根评论"),
                                            (3, "点赞子评论"),
    '''
    queryset = TaskPointModel.objects.all()
    serializer_class = TaskPointSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_object(self, to_id, to_id_type):
        return TaskPointModel.objects.get(user=self.request.user, to_id=to_id, to_id_type=to_id_type)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(to_id=kwargs['pk'], to_id_type=request.data['to_id_type'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class TaskReplyCommentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
        任务广场回答评论功能(根评论)：
        retrieve:
            获得回答评论，标明回答的id

    '''
    queryset = TaskReplyComment.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = TaskPaginationClass
    lookup_field = 'task_reply_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskReplyCommentCreateSerializer
        return TaskReplyCommentListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]
        return []

    def retrieve(self, request, *args, **kwargs):
        instance = TaskReplyComment.objects.filter(task_reply=kwargs['task_reply_id'])
        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            re_data = serializer.data
            for index, data in enumerate(re_data):
                if TaskPointModel.objects.filter(user=request.user, to_id=data['id'], to_id_type=2):
                    data['is_love'] = True
                else:
                    data['is_love'] = False
                re_data[index] = data
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class TaskReplyCommentReplyViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    任务广场回答评论功能(子评论)：
        retrieve:
            获得回答评论，标明根评论的id
    '''
    queryset = TaskReplyCommentReplyModel.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    lookup_field = 'comment_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskReplyCommentReplyCreateSerializer
        return TaskReplyCommentReplyListSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]
        return []

    def retrieve(self, request, *args, **kwargs):
        instance = TaskReplyCommentReplyModel.objects.filter(comment_id=kwargs['comment_id'])
        serializer = self.get_serializer(instance, many=True)
        re_data = serializer.data
        for index, data in enumerate(re_data):
            if TaskPointModel.objects.filter(user=request.user, to_id=data['id'], to_id_type=3):
                data['is_love'] = True
            else:
                data['is_love'] = False
            re_data[index] = data
            return Response(re_data)


class LeaveMessageViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
        retrieve:
            列出所有留言表及其回复

    '''
    # queryset = LeaveMessageModel.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    lookup_field = "send_user__id"

    def get_queryset(self):
        return LeaveMessageModel.objects.filter(receive_user=self.request.user)

    def get_permissions(self):
        if self.action == "create" or self.action == "retrieve":
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAuthenticated(), LeaveMessageReplyOwerPermision()]

    def get_serializer_class(self):
        if self.action == "create":
            return LeaveMessageCreateSerializer
        return LeaveMessageListSerializer

    def get_object(self):
        return LeaveMessageModel.objects.filter(send_user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class LeaveMessageReplyViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = LeaveMessageReplyModel.objects.all()
    permission_classes = (permissions.IsAuthenticated, LeaveMessageOwerPermision)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    lookup_field = "leaveM__id"

    def get_serializer_class(self):
        if self.action == "create":
            return LeaveMessageReplyCreateSerializer
        return LeaveMessageReplyListSerializer

    def get_object(self, id):
        return LeaveMessageReplyModel.objects.filter(leaveM_id=int(id))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object(kwargs['leaveM__id'])
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class MyTaskReplyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = MyTaskListAndRetrieveSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return TaskModel.objects.filter(task_reply__user_id=self.request.user.id)

    def get_object(self):
        return TaskModel.objects.filter(task_reply__user=self.request.user)

    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = TaskModel.objects.filter(task_reply__user=self.request.user).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # instance = self.get_object()
        instance = TaskModel.objects.filter(task_reply__user_id=self.request.user.id)
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data)


class SnippetList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        snippets = TaskReplyModel.objects.filter(user=self.request.user)
        serializer = TaskListAndRetrieveSerializer(snippets, many=True)
        re_data = serializer.data

        return Response(serializer.data)


class WangEditerImageUploadView(APIView):

    def get(self,request):
        pass

    def post(self, request, format=None):
        import os
        image = request.data["image"]
        filename = image.name
        file_bytes_io = image.file

        file = open(os.path.join(MEDIA_ROOT, filename), "wb")
        file.write(file_bytes_io.read())
        file.close()

        headers = dict()
        headers["ContentType"] = "text/html"
        headers["Charset"] = "utf-8"
        imgUrl = "http://localhost:8000" + "/media/" + filename
        res = Response(imgUrl, headers=headers)
        return res
