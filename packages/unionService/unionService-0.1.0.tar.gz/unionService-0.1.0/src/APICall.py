# -*- coding: utf-8 -*-

from urllib import request
from urllib import parse
import json
import unittest, time, re


class APICall():
    '''
    调用events记录接口
    '''

    def __init__(self):
        pass

    def apiCall(self, method, url, getparams, postparams):
        str1 = ''
        # GET方法调用
        if method == 'GET':
            if getparams != "":
                for k in getparams:
                    str1 = str1 + k + '=' + request.quote(str(getparams.get(k)))
                    if len(getparams) > 2:
                        str1 = str1 + "&"
                url = url + "&" + str1;
            result = request.urlopen(url).read()
        # POST方法调用
        if method == 'POST':
            # if postparams!="":
            data = parse.urlencode(postparams).encode("utf-8")
            req = request.Request(url, data)
            response = request.urlopen(req)
            result = response.read()
        jsdata = json.loads(result)
        return jsdata


# 单元测试继承unittest.TestCase
class GetEvents():
    def apiGet(self, base_url, params_dict):
        api = APICall()
        getparams = params_dict
        postparams = ''
        data = api.apiCall('GET', base_url, getparams, postparams)
        # # print(data)
        return data

    def apiPost(self, base_url, params_dict):
        api = APICall()
        getparams = ''
        postparams = params_dict
        # POST格式
        data = api.apiCall('POST', base_url, getparams, postparams)
        if data.get('text'):
            data = data.replace('<br>', '\n')
        # # print(data)
        return data