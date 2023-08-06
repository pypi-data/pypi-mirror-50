# coding=utf-8
import scrapy
from unionService.APICall import GetEvents
from scrapy.utils.project import get_project_settings


class JDUnion:
    host = ''

    apilists = {
        'spreadlink': {
            'url': '/jd/union/spreadlink',
            'params': {'url'}
        },
        'unionidPromotion': {
            'url': '/id/union/unionidPromotion',
            'params': {'url', 'coupon_url'}
        }
    }

    def __init__(self):
        settings = get_project_settings()
        self.host = settings.get('UNION_SERVICE_HOST')
        '''
        self.host = 'http://localhost:5580'
        '''

    def dict_merge(self,dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def call(self, key, params):
        api = self.apilists[key]

        ret = GetEvents().apiPost(self.host + api['url'], params)

        if False == ret:
            err = 'JDUion->run 远程调用失败'
            return False

        if ret['code'] & ret['code'] != 0:
            err = 'JDuion->run (%d) %s' % (ret['code'], ret['msg'])
            return False

        return ret['data']
