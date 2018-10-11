# -*- coding:utf-8 _*-  
__author__ = 'luyue'
__date__ = '2018/5/2 14:17'

import requests

def get_authorize_token():
    url = 'https://api.weibo.com/oauth2/authorize'
    client_id = 3870099249
    redirect_uri = 'http://127.0.0.1:8000/complete/weibo/'

    auth_url = url + '?client_id={client_id}&redirect_uri={redirect_uri}'.format(client_id=client_id, redirect_uri=redirect_uri)
    print(auth_url)

#http://118.24.116.137:8001/complete/weibo/?code=42ce8df0a734fc15d0f5fa54e117a317

def get_access_token(url=''):
    params = {
        'client_id':3870099249,
        'client_secret':'664c305aa0e7cc75728070f72e27b8fa',
        'grant_type':'authorization_code',
        'code':'0815eade50376172eb1a0596dcebe2c9',
        'redirect_uri':'http://127.0.0.1:8000/complete/weibo/'
    }

    res = requests.post(url=url, data=params)
    print(res.text)
    pass

#{"access_token":"2.006c8k9DdbXuNEafd6470363AYkMAB","remind_in":"157679999","expires_in":157679999,"uid":"3173205161","isRealName":"true"}


def get_usr():
    url = 'https://api.weibo.com/2/users/show.json'
    access_token = '2.006c8k9DdbXuNEafd6470363AYkMAB'
    uid = 3173205161

    usr_url = url + '?access_token={access_token}&uid={uid}'.format(access_token=access_token, uid=uid)
    print(usr_url)


if __name__ == '__main__':
    get_authorize_token()
    # get_access_token(url='https://api.weibo.com/oauth2/access_token')
    # get_usr()