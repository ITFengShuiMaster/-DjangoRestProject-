# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/11 22:45'

from rest_framework import permissions

SAFE_METHODS = ('HEAD', 'OPTIONS')


class IsTeacherPermision(permissions.BasePermission):
    '''
    自定义权限:是否具有老师身份
    '''
    def has_permission(self, request, view):
        if request.user.row_id == 'tea_owner':
            return True
        return False


class IsSuperPermision(permissions.BasePermission):
    '''
    自定义权限:是否具有超级用户权限
    '''
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwerPermision(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user


class UserInfoOwerPermision(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        flag = obj == request.user
        return obj == request.user


class LeaveMessageOwerPermision(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        flag = obj == request.user
        return obj.user == request.user


class LeaveMessageReplyOwerPermision(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        flag = obj == request.user
        return obj.receive_user == request.user
