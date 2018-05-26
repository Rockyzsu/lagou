# -*-coding=utf-8-*-

__author__ = 'Rocky'
'''
http://30daydo.com
Email: weigesysu@qq.com
'''
from scrapy import signals
import time
import hashlib

class ProxyMiddlewares(object):
    def process_request(self, request, spider):
        # time.sleep(1)
        auth_header = self.get_auth_header()
        request.meta['proxy'] = "http://s3.proxy.mayidaili.com:8123"
        request.headers['Proxy-Authorization'] = auth_header

    def get_auth_header(self):
        # 请替换app_key和secret
        app_key = "67783764"
        secret = "6151eb360668ca10ad772ca9e46d306b"

        param_map = {
            "app_key": app_key,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),  # 如果你的程序在国外，请进行时区处理
            "enable-simulate": 'true',
            "random-useragent": 'pc',
            "clear-cookies": 'true'
        }
        # 排序
        keys = param_map.keys()
        keys.sort()

        codes = "%s%s%s" % (secret, str().join('%s%s' % (key, param_map[key]) for key in keys), secret)

        # 计算签名
        sign = hashlib.md5(codes).hexdigest().upper()

        param_map["sign"] = sign

        # 拼装请求头Proxy-Authorization的值
        keys = param_map.keys()
        auth_header = "MYH-AUTH-MD5 " + str('&').join('%s=%s' % (key, param_map[key]) for key in keys)

        # print time.strftime("%Y-%m-%d %H:%M:%S")
        # print authHeader

        return auth_header