# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/22 14:51'

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import uuid

def return_token():
    AccessKey = 'ueydTjsLS3akQ5jTgZXNsWo8y7CPygsFPpT9fuZ3'
    SecretKey = '0cSK9vOl-s6cf16qRh_vP1ffiILPL2gRMWfgTzWG'
    Bucket_Name = 'agriculture-first'
    q = Auth(AccessKey, SecretKey)
    token = q.upload_token(Bucket_Name, None, 3600)
    return token


def upload_video(video_file_url):
    access_key = 'ueydTjsLS3akQ5jTgZXNsWo8y7CPygsFPpT9fuZ3'
    secret_key = '0cSK9vOl-s6cf16qRh_vP1ffiILPL2gRMWfgTzWG'
    bucket_name = 'agriculture-first'
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    # 上传到七牛后保存的文件名
    key_name = str(uuid.uuid1())
    key = key_name
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)
    # 要上传文件的本地路径
    localfile = video_file_url
    ret, info = put_file(token, key, localfile)
    print("info:-----",info)
    print("ret:-----", ret)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    return ret['key']


if __name__ == "__main__":
    upload_video(r'D:\Agricultural_Culture\Agri\media\video\2018\05\test1.mp4')
    import os
    os.path.abspath()