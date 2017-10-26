# -*-coding=utf-8-*-
import json

import scrapy
import redis
from lagou.items import CompanyItem


class CompanyInfo(scrapy.Spider):
    name = 'company'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.totalCount = 56
        self.datas = {"first": "false",
                      "pn": "3",
                      "sortField": "0",
                      "havemark": "0"}

        self.headers = {'Origin': 'https://www.lagou.com', 'Content-Length': '39',
                        'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate, br',
                        'X-Anit-Forge-Code': '0', 'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': 'None',
                        'Host': 'www.lagou.com', 'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
                        'Connection': 'keep-alive',
                        # 'Cookie': 'user_trace_token=20171008235700-51c89e1e-ac41-11e7-822c-525400f775ce; LGUID=20171008235700-51c8a17f-ac41-11e7-822c-525400f775ce; JSESSIONID=ABAAABAACDBABJB2B423D18B13E1DA9574E04C3A67D18CB; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; TG-TRACK-CODE=index_company; LGSID=20171022205613-622e2f35-b728-11e7-a438-525400f775ce; LGRID=20171022205618-65283f3a-b728-11e7-9601-5254005c3644; _putrc=DFAF58A586D854B0; login=true; unick=%E9%99%88%E9%94%A6%E4%BC%9F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=138; index_location_city=%E6%B7%B1%E5%9C%B3; _gid=GA1.2.1723890745.1508676965; _ga=GA1.2.891768125.1507478204; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508000182,1508164186,1508336224,1508676965; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1508676974',
                        'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        self.new_cookie = {"user_trace_token": "20171008235700-51c89e1e-ac41-11e7-822c-525400f775ce",
                           "LGUID": "20171008235700-51c8a17f-ac41-11e7-822c-525400f775ce",
                           "JSESSIONID": "ABAAABAACDBABJB2B423D18B13E1DA9574E04C3A67D18CB",
                           "_gat": "1",
                           "PRE_UTM": "",
                           "PRE_HOST": "",
                           "PRE_SITE": "",
                           "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
                           "TG-TRACK-CODE": "index_company",
                           "LGSID": "20171022205613-622e2f35-b728-11e7-a438-525400f775ce",
                           "LGRID": "20171022205618-65283f3a-b728-11e7-9601-5254005c3644",
                           "_putrc": "DFAF58A586D854B0",
                           "login": "true",
                           "unick": "%E9%99%88%E9%94%A6%E4%BC%9F",
                           "showExpriedIndex": "1",
                           "showExpriedCompanyHome": "1",
                           "showExpriedMyPublish": "1",
                           "hasDeliver": "138",
                           "index_location_city": "%E6%B7%B1%E5%9C%B3",
                           "_gid": "GA1.2.1723890745.1508676965",
                           "_ga": "GA1.2.891768125.1507478204",
                           "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1508000182,1508164186,1508336224,1508676965",
                           "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1508676974" }
        self.define_cookie = {'user_trace_token': '20160612223035-3a02d006-30aa-11e6-a343-5254005c3644',
                              'LGUID': '20160612223035-3a02d566-30aa-11e6-a343-5254005c3644',
                              'PRE_UTM': '',
                              'PRE_HOST': '',
                              'PRE_SITE': '',
                              'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                              'showExpriedIndex': '1',
                              'showExpriedCompanyHome': '1',
                              'showExpriedMyPublish': '1',
                              'hasDeliver': '124',
                              'index_location_city': '%E6%B7%B1%E5%9C%B3',
                              'login': 'false',
                              'unick': '""',
                              '_putrc': '""',
                              'JSESSIONID': 'ABAAABAACDBAAIAF33B4C87F595BE43FE5DBD6846EA46FE',
                              '_gat': '1',
                              'SEARCH_ID': 'ab601b73c41e433b9585f11d13253dab',
                              '_gid': 'GA1.2.1335763621.1507978370',
                              '_ga': 'GA1.2.499625224.1465741835',
                              'LGSID': '20171014185251-d2e2289c-b0cd-11e7-9550-5254005c3644',
                              'LGRID': '20171014191037-4e4ec5c5-b0d0-11e7-9550-5254005c3644',
                              'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1507809365,1507978370',
                              'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1507979436',
                              'TG-TRACK-CODE': 'hpage_code'}

        self.cookie = {'user_trace_token': '20171008235700-51c89e1e-ac41-11e7-822c-525400f775ce',
                       'LGUID': '20171008235700-51c8a17f-ac41-11e7-822c-525400f775ce',
                       'JSESSIONID': 'ABAAABAACDBABJB2B423D18B13E1DA9574E04C3A67D18CB',
                       '_gat': '1',
                       'PRE_UTM': '',
                       'PRE_HOST': '',
                       'PRE_SITE': '',
                       'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F',
                       'TG-TRACK-CODE': 'index_company',
                       'LGSID': '20171022205613-622e2f35-b728-11e7-a438-525400f775ce',
                       'LGRID': '20171022205618-65283f3a-b728-11e7-9601-5254005c3644',
                       '_putrc': 'DFAF58A586D854B0',
                       'login': 'true',
                       'unick': '%E9%99%88%E9%94%A6%E4%BC%9F',
                       'showExpriedIndex': '1',
                       'showExpriedCompanyHome': '1',
                       'showExpriedMyPublish': '1',
                       'hasDeliver': '138',
                       'index_location_city': '%E6%B7%B1%E5%9C%B3',
                       '_gid': 'GA1.2.1723890745.1508676965',
                       '_ga': 'GA1.2.891768125.1507478204',
                       'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1508000182,1508164186,1508336224,1508676965',
                       'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1508676974'}
        self.url = 'https://www.lagou.com/gongsi/215-0-0.json'

    def start_requests(self):
        for i in range(2, 7):
            # self.data['pn'] = str(i)
            meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
            yield scrapy.FormRequest(url=self.url, headers=self.headers, callback=self.parse,
                                     formdata=self.datas,
                                     dont_filter=True,)

    def parse(self, response):
        js = json.loads(response.body)
        print js
        for i in js['result']:
            item = CompanyItem()
            print i['companyId'], i['companyFullName']
            item['companyId'] = i['companyId']
            item['companyFullName'] = i['companyFullName']
            yield item
