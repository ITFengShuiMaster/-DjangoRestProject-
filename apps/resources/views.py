from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework import pagination
from rest_framework.renderers import JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import TextModel
from .serializers import TextFileSerializer, TextFileListSerializer
from utils.permissions import IsOwerPermision
from Agri.settings import IP_KEY

import os

# Create your views here.


class UTF8JSONResponse(JSONRenderer):
    charset = 'utf-8'


class VideoPagination(pagination.PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'


class TextFileViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    文档上传接口:
    list:
        显示所有文档(包含了在线预览的pdf地址)
    create:
        用户上传文档
    destroy:
        删除上传文档（限指定用户)(测试中，暂时用不了)
    '''
    queryset = TextModel.objects.all()
    # serializer_class = TextFileSerializer
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    pagination_class = VideoPagination

    def get_permissions(self):
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsOwerPermision()]
        return [permissions.IsAuthenticated(),]

    def get_serializer_class(self):
        if self.action == 'list':
            return TextFileListSerializer
        return TextFileSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            for index, re_data in enumerate(serializer.data):
                # http://dcsapi.com?k=340251117&url=http://172.19.73.39:8001/media/text/2018/04/20/1515001103卢越.docx
                return_file_path = re_data['text']
                re_data['pdf_path'] = 'http://dcsapi.com?k={0}&url='.format(IP_KEY) + return_file_path
                serializer.data[index] = re_data
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for index, re_data in enumerate(serializer.data):
            #http://dcsapi.com?k=340251117&url=http://172.19.73.39:8001/media/text/2018/04/20/1515001103卢越.docx
            return_file_path = re_data['text']
            re_data['pdf_path'] = 'http://dcsapi.com?k={0}&url='.format(IP_KEY)+return_file_path
            serializer.data[index] = re_data

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        file_name = instance.text.file.name
        instance_file_name = instance.text.name[instance.text.name.rfind(r'/')+1:]

        file_size = round(os.path.getsize(file_name)/1024/1024, 2)
        instance.file_size = str(file_size)+'M' if file_size > 1 else str(file_size*1024)+'KB'
        instance.file_name = instance_file_name
        instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()
