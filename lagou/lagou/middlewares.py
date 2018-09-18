# -*-coding=utf-8-*-

# @Time : 2018/9/15 19:45
# @File : middlewares.py
import redis
import requests
import time
from lagou  import config

class ProxiesMiddleware(object):

    def __init__(self):
        self.rds = redis.StrictRedis(config.redis_host, db=config.db, decode_responses=True)
    def process_request(self, request, spider):

        proxyServer = self.proxy_redis()
        request.meta["proxy"] = proxyServer

    def get_proxy(self, retry=50):
        proxyurl = 'http://{}:8081/dynamicIp/common/getDynamicIp.do'.format(config.proxyip)
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


    def proxy_redis(self):
        proxy = self.rds.randomkey()
        return 'http://{}'.format(proxy)