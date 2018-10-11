# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/4/8 16:55'

from Agri.settings import YUN_PIAN_URL, API_KEY


class YunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_url = YUN_PIAN_URL

    def send_code(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile':mobile,
            'text':'【智慧农业产学平台】欢迎注册智慧农业产学研，您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        import requests
        import json
        response =requests.post(self.single_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict


class ResetYunPian(object):
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_url = YUN_PIAN_URL

    def send_code(self, code, mobile):
        params = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '【智慧农业产学平台】您的验证码是#code#。如非本人操作，请忽略本短信'.format(code=code)
        }
        import requests
        import json
        response = requests.post(self.single_url, data=params)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == '__main__':
    re = ResetYunPian(API_KEY)
    re.send_code(code='1011', mobile='13270710661')