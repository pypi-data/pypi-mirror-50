# coding=utf-8
import scrapy
from unionService.APICall import GetEvents
from scrapy.utils.project import get_project_settings


class Dingdanxia:
    apikey = ''
    signature = False

    apilists = {
        'uland_query': {
            'url': 'http://api.tbk.dingdanxia.com/tbk/uland_query',
            'params': {'url'}
        },
        'id_privilege': {
            'url': 'http://api.tbk.dingdanxia.com/tbk/id_privilege',
            'params': {'id', 'tpwd'}
        }
    }

    def __init__(self):
        settings = get_project_settings()
        self.apikey = settings.get('DDX_TBK_KEY')
        '''
        self.apikey = 'tobereplaced'
        '''

    def dict_merge(self,dict1, dict2):
        res = {**dict1, **dict2}
        return res

    def call(self, key, params):
        api = self.apilists[key]

        params_dict = {'apikey': self.apikey}
        ret = GetEvents().apiPost(api['url'], self.dict_merge(params_dict, params))

        if False == ret:
            err = 'Dingdanxia->run 远程调用失败'
            return False

        if ret['code'] & ret['code'] != 200:
            err = 'Dingdanxia->run (%d) %s' % (ret['code'], ret['msg'])
            return False

        return ret['data']
