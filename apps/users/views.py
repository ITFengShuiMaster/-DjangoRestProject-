from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.views import JSONWebTokenAPIView, ObtainJSONWebToken
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import JSONWebTokenSerializer

# jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

from .serializers import SemVerifycodeSerializers, UserRegSerializer, UserProfileSerializer, TestImageSerializer,\
    PasswordResetSerializer, UserInfoSerializer, UserProfileUpdateSerializer, ZWP_UserInfoSerializer
from .models import VerifyCode, UserInfo
from utils.yunpian import YunPian, ResetYunPian
from utils.permissions import UserInfoOwerPermision
from Agri.settings import API_KEY, BASE_DIR

from datetime import datetime
import os, base64

User = get_user_model()
# Create your views here.


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token,
        'user_id': user.id
    }


class CustomBackend(ModelBackend):
    '''
    自定义用户登录
    '''
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except:
            return None


class UserJWTLoginView(JSONWebTokenAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    token,
                                    expires=expiration,
                                    httponly=True)
            return response
        #自定义修改
        errors = serializer.errors
        errors['error'] = '用户名或密码错误'
        del errors['non_field_errors']
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class UserObtainJSONWebToken(UserJWTLoginView):
    serializer_class = JSONWebTokenSerializer


class SemVerifyCodeSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    发送验证码接口
    '''
    serializer_class = SemVerifycodeSerializers

    def random_code(self):
        '''
        生成验证码
        :param:
        :return:
        '''
        from random import choice
        ran_code = []
        seems = '123456789'
        for i in range(4):
            ran_code.append(choice(seems))

        return ''.join(ran_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        code = self.random_code()
        code_type = serializer.validated_data['code_type']
        if code_type == 'register':
            send_yun = YunPian(API_KEY)
            re_dict = send_yun.send_code(code=code, mobile=mobile)
        else:
            send_yun = ResetYunPian(API_KEY)
            re_dict = send_yun.send_code(code=code, mobile=mobile)

        if not re_dict['code'] == 0:
            return Response({
                "mobile": re_dict['msg']
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            verify_code = VerifyCode(mobile=mobile, code=code, code_type=code_type)
            verify_code.save()
            headers = self.get_success_headers(serializer.data)
            return Response({"mobile": mobile}, status=status.HTTP_201_CREATED, headers=headers)


class UserRegViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    create:
    用户注册接口
    retrieve:
    用户个人信息接口, id为用户名即手机号
    update:
    用户更新信息接口， id为用户名即手机号
    '''
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    # lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            return [permissions.IsAuthenticated(), UserInfoOwerPermision()]
        return []

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegSerializer
        elif self.action == 'retrieve':
            return UserProfileSerializer
        return UserProfileSerializer

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class PasswordResetViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    忘记密码接口
    update:
        id字段的值任意
    partial_update:
        不要在意这个接口，不用
    '''
    queryset = User.objects.all()
    serializer_class = PasswordResetSerializer

    def get_object(self):
        return User.objects.get(mobile=self.request.data['username'])


class UserInfoUpdateViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_object(self):
        return self.request.user.user_profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ZWP_UpdateUserInfoView(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = ZWP_UserInfoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_object(self):
        return self.request.user.user_profile

    # def update(self, request, *args, **kwargs):
    #     import datetime
    #     instance = self.get_object()
    #     data = request.data
    #     instance.sex = data['sex'][1:-1]
    #     instance.image = data['image'][1:-1]
    #     birth = data['birth'][1:-1]
    #     instance.birth = datetime.datetime.strptime(birth, '%Y-%m-%d')
    #     instance.address = data['address'][1:-1]
    #     instance.nick_name = data['nick_name'][1:-1]
    #     instance.save()
    #     return Response({"status":"OK"}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data
        re_data = dict()
        re_data['sex'] = data['sex'][1:-1]
        re_data['image'] = data['image'][1:-1]
        re_data['birth'] = data['birth'][1:-1]
        re_data['address'] = data['address'][1:-1]
        re_data['nick_name'] = data['nick_name'][1:-1]

        serializer = self.get_serializer(instance, data=re_data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class TestViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = TestImageSerializer
