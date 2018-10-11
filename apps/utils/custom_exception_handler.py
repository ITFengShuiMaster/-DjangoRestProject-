# -*- coding:utf-8 _*-
from django.db import ProgrammingError

__author__ = 'luyue'
__date__ = '2018/5/31 10:24'

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response is not None:
    #     response.data['status_code'] = response.status_code
    try:
        if exc.default_code == 'not_authenticated':
            response.data['detail'] = "您未登录，请先登录!"
            response.data['url'] = "/login/"

        if exc.default_code == "invalid":
            response.data['status'] = response.status_code
            response.status_code = 200

        if exc.default_code == "permission_denied":
            response.data['status'] = response.status_code
            response.status_code = 200
        return  response
    except Exception as e:
        return response