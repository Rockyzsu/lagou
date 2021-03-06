# -*-coding=utf-8-*-

# @Time : 2018/9/15 19:45
# @File : middlewares.py
import redis
import requests
import time
from lagou  import config

class ProxiesMiddleware(object):

    def process_request(self, request, spider):
        proxyServer = self.get_proxy()
        request.meta["proxy"] = proxyServer

    def get_proxy(self, retry=5):
        proxyurl = 'http://{}:8101/dynamicIp/common/getDynamicIp.do'.format(config.proxyip)
        for i in range(1, retry + 1):
            try:
                r = requests.get(proxyurl, timeout=10)
            except Exception as e:
                print(e)
                print('Failed to get proxy ip, retry ' + str(i))
                time.sleep(1)
            else:
                js = r.json()
                proxyServer = 'http://{0}:{1}'.format(js.get('ip'), js.get('port'))
                return proxyServer

        return None

    def high_proxy(self):
        url='http://39.108.59.38:7772/Tools/proxyIP.ashx?OrderNumber=10292c8277746dbf62bddc40e1583044&poolIndex=85323&cache=1&qty=1'
        r = requests.get(url)
        s=r.text()
        return 'http://'+s.strip()


class RedirectMiddleware(object):

    def response_request(self,):
        pass