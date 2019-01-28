# -*-coding=utf-8-*-
import json

import pymongo
import scrapy
import redis, collections
from lagou.items import CompanyItem


# 获取公司ID 这种方式，所有公司的id只有1000家
class CompanyInfo(scrapy.Spider):
    name = 'company'
    allowed_domains = ['lagou.com']

    def __init__(self):
        super(CompanyInfo,self).__init__()
        # 230 东莞
        # 深圳
        self.city = [230]
        #  获取更多城市，替换213 这个数字就可以， 根据不同城市填写
        self.url = 'https://www.lagou.com/gongsi/{}-0-0.json'

        self.datas = collections.OrderedDict({"first": "false",
                                              "pn": "",
                                              "sortField": "0",
                                              "havemark": "0"}
                                             )

        self.headers = {
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'application/json, text/javascript, */*; q=0.01', 'Connection': 'keep-alive',
            'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        self.first_headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01',
                              'Accept-Encoding': 'gzip,deflate,br', 'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8',
                              'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
                              'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                              'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
                              'Referer': 'https://www.lagou.com/gongsi/{}-0-0-0',
                              'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
                              'X-Anit-Forge-Code': '0',
                              'X-Anit-Forge-Token': 'None',
                              'X-Requested-With': 'XMLHttpRequest'
                              }

        self.cookies = {"JSESSIONID": "ABAAABAAAGFABEF8B7F2F7B6456E459FEF825D0DBB1FAAE",
                        "user_trace_token": "20181119184953-f8b2ed00-c305-48a2-b797-99ec6c2809a4",
                        "_ga": "GA1.2.1290529047.1542624594",
                        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542624594",
                        "LGUID": "20181119184956-da92a9a5-ebe8-11e8-a727-525400f775ce",
                        "_gid": "GA1.2.41473263.1542781721",
                        "LGSID": "20181121142839-aeed2262-ed56-11e8-b119-525400f775ce",
                        "index_location_city": "%E5%85%A8%E5%9B%BD",
                        "TG-TRACK-CODE": "index_company",
                        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542782542",
                        "LGRID": "20181121144220-98b2f1f8-ed58-11e8-8a9b-5254005c3644", }

        self.doc = pymongo.MongoClient('10.18.6.26', port=27001)['db_parker']['lagou_company']

    def start_requests(self):
        yield scrapy.http.Request(
            url='https://www.lagou.com/gongsi/',
            headers=self.first_headers,
            callback=self.next_request,
            # meta={'cookiejar': True},
            dont_filter=True
        )

    def next_request(self, response):

        for city in self.city:
            # print response.body
            # 公司没那么多，只需填一个小于100的,一般只有20页
            headers=self.first_headers.copy()
            headers['Referer']=headers['Referer'].format(city)
            for i in range(1, 100):
                self.datas['pn'] = str(i)

                meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
                yield scrapy.http.FormRequest(url=self.url.format(city), headers=headers,
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

        except Exception as e:
            print(e)
            return
        if len(js['result']) == 0:
            print('公司列表为空')
            return

        # for i in js['result']:
        # item = CompanyItem()
        # item['companyId'] = i['companyId']
        # item['companyFullName'] = i['companyFullName']
        # yield item
        # 直接插入数据库
        try:
            self.doc.insert_many(js['result'])
        except Exception as e:
            print('写入mongo错误{}'.format(e))
