# -*-coding=utf-8-*-
import json

import scrapy
import redis, collections
from lagou.items import CompanyItem


class CompanyInfo(scrapy.Spider):
    name = 'company'
    allowed_domains = ['lagou.com']

    def __init__(self):

        #  获取更多城市，替换213 这个数字就可以， 根据不同城市填写
        self.url = 'https://www.lagou.com/gongsi/215-0-0.json'

        self.datas = collections.OrderedDict({"first": "false",
                                              "pn": "",
                                              "sortField": "0",
                                              "havemark": "0"}
                                             )

        self.headers = {'Content-Length': '39', 'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Accept': 'application/json, text/javascript, */*; q=0.01', 'Connection': 'keep-alive',
                        'Cache-Control': 'no-cache', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}

        self.first_headers = {'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate, br',
                              'Host': 'www.lagou.com',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                              'Upgrade-Insecure-Requests': '1', 'Connection': 'keep-alive',
                              'Cookie': 'user_trace_token=20160612223035-3a02d006-30aa-11e6-a343-5254005c3644; LGUID=20160612223035-3a02d566-30aa-11e6-a343-5254005c3644; JSESSIONID=ABAAABAACDBAAIA2AF78F3B190ED86CE3AD74D3F50F274F; X_HTTP_TOKEN=ae3de20baf406224ec17647191d91609; _putrc=DFAF58A586D854B0; login=true; unick=%E9%99%88%E9%94%A6%E4%BC%9F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=138; TG-TRACK-CODE=index_search; SEARCH_ID=08c78425fe834aad93ccda9367e90b39; index_location_city=%E6%B7%B1%E5%9C%B3; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1507809365,1507978370,1508072067,1509002344; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1509022033; _gat=1; LGSID=20171026201121-c740dde5-ba46-11e7-9626-5254005c3644; LGRID=20171026204711-c914afe5-ba4b-11e7-9626-5254005c3644; _ga=GA1.2.499625224.1465741835; _gid=GA1.2.1667060466.1509002344',
                              'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                              'Referer': 'https://www.lagou.com/gongsi/j917.html',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

        self.cookies = {"user_trace_token": "20160612223035-3a02d006-30aa-11e6-a343-5254005c3644",
                        "LGUID": "20160612223035-3a02d566-30aa-11e6-a343-5254005c3644",
                        "JSESSIONID": "ABAAABAACDBAAIA2AF78F3B190ED86CE3AD74D3F50F274F",
                        "X_HTTP_TOKEN": "ae3de20baf406224ec17647191d91609",
                        "_putrc": "DFAF58A586D854B0",
                        "login": "true",
                        "unick": "%E9%99%88%E9%94%A6%E4%BC%9F",
                        "showExpriedIndex": "1",
                        "showExpriedCompanyHome": "1",
                        "showExpriedMyPublish": "1",
                        "hasDeliver": "138",
                        "TG-TRACK-CODE": "index_search",
                        "SEARCH_ID": "08c78425fe834aad93ccda9367e90b39",
                        "index_location_city": "%E6%B7%B1%E5%9C%B3",
                        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1507809365,1507978370,1508072067,1509002344",
                        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1509022033",
                        "_gat": "1",
                        "LGSID": "20171026201121-c740dde5-ba46-11e7-9626-5254005c3644",
                        "LGRID": "20171026204711-c914afe5-ba4b-11e7-9626-5254005c3644",
                        "_ga": "GA1.2.499625224.1465741835",
                        "_gid": "GA1.2.1667060466.1509002344", }

    def start_requests(self):
        yield scrapy.http.Request(url='https://www.lagou.com/gongsi/', headers=self.first_headers,
                                  callback=self.next_request,
                                  meta={'cookiejar': 1}
                                  )

    def next_request(self, response):
        # print response.body
        #公司没那么多，只需填一个小于100的
        for i in range(1, 100):
            self.datas['pn'] = str(i)
            meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]}
            yield scrapy.http.FormRequest(url=self.url, headers=self.first_headers, callback=self.parse_item,
                                          formdata=self.datas,
                                          cookies=self.cookies,
                                          # meta={'cookiejar': response.meta['cookiejar'],'dont_redirect': True, 'handle_httpstatus_list': [302]},
                                          # meta={'cookiejar': response.meta['cookiejar']},
                                          # meta={'dont_merge_cookies': True},
                                          dont_filter=True)

    def parse_item(self, response):
        try:
            js = json.loads(response.body)
            print js
            # print js
        except Exception, e:
            print e
            return
        if len(js['result']) == 0:
            print 'empty'
            return
        for i in js['result']:
            item = CompanyItem()
            # print i['companyId'], i['companyFullName']
            item['companyId'] = i['companyId']
            item['companyFullName'] = i['companyFullName']
            yield item
