"""
Lsky图床接口类
"""
import json
import random

import requests


class LskyApi:
    _API_BASE = 'http://124.227.1.192:53008/api/v1'
    _Accept = 'application/json'
    """===============
    "初始化数据
    """
    def __int__(self, API_BASE):
        if API_BASE is not None:
            self._API_BASE = API_BASE
        else:
            self._API_BASE = 'http://124.227.1.192:53008/api/v1'
        self._TOKEN = None
    """
        获取token
    """
    def tokens(self, email, passwd):
        # method = 'POST'
        token_api = '/tokens'
        params = dict()
        params['email'] = email
        params['password'] = passwd
        token_api_full = self._API_BASE + token_api
        res = requests.post(token_api_full, params=params)

        if res.status_code == 200:
            result_json = json.loads(res.text)
            LskyApi._TOKEN = result_json['data']['token']
        else:
            result_json = None
            LskyApi._TOKEN = result_json
        return result_json
    """
        获取存储策略
    """
    def strategies(self, keyword):
        pass
    """
        上传图片
    """
    def upload(self, file_path):
        method = 'POST'
        # this_heard = 'Content-Type'
        headers = {
            "Authorization": 'Bearer ' + self._TOKEN,
            'Accept': LskyApi._Accept,
            'Content-Type': 'multipart/form-data',
            'Boundary': '-----' + self._TOKEN
        }
        upload_api = '/upload'
        payload = {'Boundary': '-----' + self._TOKEN}
        files = [('file', (file_path, open(file_path, 'rb'), 'image/jpeg'))]
        upload_api_full = self._API_BASE + upload_api
        res = requests.request(method=method, url=upload_api_full, data=payload, files=files, )
        if res.status_code == 200:
            return_json = json.loads(res.text)
        else:
            return_json = None
            print(res)
        return return_json


if __name__ == '__main__':
    lskyApi = LskyApi()
    lskyApi.tokens('18697998680@163.com', '')
    res_json = lskyApi.upload('E:\\datas\\systems\\pictures\\background\\r1.jpg')
    if res_json is not None:
        print(res_json['data'])
        print(res_json['data']['links']['markdown'])
