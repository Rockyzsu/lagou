# -*-coding=utf-8-*-
import json

import scrapy
import redis, collections
from lagou.items import CompanyItem


class CompanyInfo(scrapy.Spider):
    name = 'company'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.citys = [213, 2, 3, 6, 184, 252]
        #  获取更多城市，替换213 这个数字就可以， 根据不同城市填写
        self.url = 'https://www.lagou.com/gongsi/{}-0-0.json'

        self.datas = collections.OrderedDict({"first": "false",
                                              "pn": "",
                                              "sortField": "0",
                                              "havemark": "0"}
                                             )

        self.headers = {
            # 'Content-Length': '39',
            # 'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01', 'Connection': 'keep-alive',
            'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        self.first_headers = {
            # 'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate, br',
            'Host': 'www.lagou.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Cookie': 'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644; LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644; _ga=GA1.2.1514235968.1511234812; JSESSIONID=ABAAABAACBHABBI1A2002B1D4BE797A9348546D9AF5EF2A; _gid=GA1.2.1655607353.1527327820; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527327829; index_location_city=%E5%85%A8%E5%9B%BD; SEARCH_ID=fa68e1ccb6904d33bf9eb657173121ab; TG-TRACK-CODE=gongsi_banner; LGSID=20180526232211-900a8947-60f8-11e8-8c26-5254005c3644; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527350122; LGRID=20180526235527-35b6c072-60fd-11e8-a4c7-525400f775ce',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            # 'Referer': 'https://www.lagou.com/gongsi/{}-0-0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }

        self.cookies = {
            "user_trace_token": "20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644",
            "LGUID": "20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644",
            "_ga": "GA1.2.1514235968.1511234812",
            "JSESSIONID": "ABAAABAACBHABBI1A2002B1D4BE797A9348546D9AF5EF2A",
            "_gid": "GA1.2.1655607353.1527327820",
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1527327829",
            "index_location_city": "%E5%85%A8%E5%9B%BD",
            "SEARCH_ID": "fa68e1ccb6904d33bf9eb657173121ab",
            "TG-TRACK-CODE": "gongsi_banner",
            "LGSID": "20180526232211-900a8947-60f8-11e8-8c26-5254005c3644",
            "_gat": "1",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1527350122",
            "LGRID": "20180526235527-35b6c072-60fd-11e8-a4c7-525400f775ce", }

    def start_requests(self):
        yield scrapy.http.Request(
            url='https://www.lagou.com/gongsi/',
            headers=self.first_headers,
            callback=self.next_request,
            meta={'cookiejar': True}
        )

    def next_request(self, response):

        for city in self.citys:
            # print response.body
            # 公司没那么多，只需填一个小于100的
            for i in range(1, 100):
                self.datas['pn'] = str(i)
                meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
                yield scrapy.http.FormRequest(url=self.url.format(city), headers=self.first_headers,
                                              callback=self.parse_item,
                                              formdata=self.datas,
                                              cookies=self.cookies,
                                              # meta={'cookiejar': response.meta['cookiejar'],'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                              # meta={'cookiejar': response.meta['cookiejar']},
                                              # meta={'dont_merge_cookies': True},
                                              dont_filter=True
                                              )

    def parse_item(self, response):
        try:
            js = json.loads(response.body)
            # print(js)
            # print js
        except Exception as e:
            print(e)
            return
        if len(js['result']) == 0:
            print('公司列表为空')
            return

        for i in js['result']:
            item = CompanyItem()
            item['companyId'] = i['companyId']
            item['companyFullName'] = i['companyFullName']
            yield item
