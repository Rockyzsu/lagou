# -*-coding=utf-8-*-
import json

import re

import datetime
from lagou.items import LagouItem
import scrapy
from lagou.models import DBSession, Jobs
import redis


class lagouspider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.years = str(datetime.datetime.now().year)
        self.pool = redis.Redis(host='localhost', port=6379, db=3)
        self.cookies = {"user_trace_token": "20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644",
                        "LGUID": "20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644",
                        "_ga": "GA1.2.1514235968.1511234812",
                        "LG_LOGIN_USER_ID": "dc82d3e8edcc06f3ee143961873c3ba4ad0d8fe42571bced",
                        "showExpriedIndex": "1",
                        "showExpriedCompanyHome": "1",
                        "showExpriedMyPublish": "1",
                        "hasDeliver": "185",
                        "index_location_city": "%E5%85%A8%E5%9B%BD",
                        "JSESSIONID": "ABAAABAAAIAACBI2ECE0109F68209B809158B7527D94550",
                        "_gat": "1",
                        "LGSID": "20180630002925-9647d11f-7bb9-11e8-9775-5254005c3644",
                        "PRE_UTM": "",
                        "PRE_HOST": "",
                        "PRE_SITE": "",
                        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
                        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1528596582,1528982025,1530191868,1530289763",
                        "_gid": "GA1.2.174424791.1530289763",
                        "_putrc": "DFAF58A586D854B0",
                        "login": "true",
                        "unick": "%E9%99%88%E9%94%A6%E4%BC%9F",
                        "gate_login_token": "226fd311bb36716586af059cad241b17f6e826f13d4bd66c",
                        "TG-TRACK-CODE": "index_company",
                        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1530289774",
                        "LGRID": "20180630002937-9d3e7818-7bb9-11e8-9775-5254005c3644", }
        self.url = 'https://www.lagou.com/gongsi/searchPosition.json'
        # self.session = DBSession()
        # self.pool=redis.Redis()

    def start_requests(self):
        # obj = self.session.query(Company).all()
        obj = self.pool.keys()
        for i in obj:
            headers = {
                'Origin': 'https://www.lagou.com',
                'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6', 'Accept-Encoding': 'gzip, deflate, br',
                'X-Requested-With': 'XMLHttpRequest',
                'Host': 'www.lagou.com',
                'Accept': 'application/json, text/javascript, */*; q=0.01',

                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                'Connection': 'keep-alive',

                'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
                'Referer': 'https://www.lagou.com/gongsi/j%s.html' % i,
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }

            data = {'companyId': str(i),
                    'positionFirstType': u'全部',
                    'schoolJob': 'false',
                    'pageNo': '1',
                    'pageSize': '10'}
            yield scrapy.http.FormRequest(
                url=self.url,
                headers=headers,
                formdata=data,
                callback=self.parse,
                cookies=self.cookies,
                dont_filter=True,
                meta={'headers': headers, 'data': data}
            )

    def parse(self, response):
        print(response.text)
        js = json.loads(response.body)
        headers = response.meta['headers']
        data = response.meta['data']
        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = (totalCount + 10) / 10
        for i in range(1, page + 1):
            data['pageNo'] = str(i)
            print('page: ', i)
            yield scrapy.FormRequest(url=self.url,
                                     headers=headers,
                                     callback=self.parse_data,
                                     formdata=data,
                                     cookies=self.cookies, dont_filter=True)

    def parse_data(self, response):
        # print(response)
        js = json.loads(response.body)

        try:
            results = js.get('content').get('data').get('page').get('result')
        except:
            return

        if not results:
            print('empty')
            return
        for i in results:
            # 13k-25k
            item = LagouItem()
            item['companyId'] = i.get('companyId')
            item['positionId'] = i.get('positionId')
            item['jobNature'] = i.get('jobNature')
            item['companyName'] = i.get('companyName')
            item['financeStage'] = i.get('financeStage')
            item['companyFullName'] = i.get('companyFullName')
            item['companySize'] = i.get('companySize')
            item['industryField'] = i.get('industryField')
            item['positionName'] = i.get('positionName')
            item['city'] = i.get('city')
            createTime = i.get('createTime')
            try:
                if not re.search(self.years, createTime):
                    createTime = datetime.datetime.now().strftime('%Y-%m-%d') + ' ' + createTime

            except Exception as e:
                print(e)
                # print createTime

            item['createTime'] = createTime

            s = i.get('salary')
            try:
                if re.search('-', s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')
                    item['salary_low'] = int(s.split('-')[0].replace('k', '000'))
                    item['salary_high'] = int(s.split('-')[1].replace('k', '000'))
                elif re.search(u'以上', s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')

                    item['salary_low'] = int(re.findall('(\d+)k', s)[0])
                    item['salary_high'] = int(re.findall('(\d+)k', s)[0])



            except Exception as e:
                print('its salary')
                print(i.get('salary'))
                print(e)
            item['workYear'] = i.get('workYear')
            item['education'] = i.get('education')
            item['positionAdvantage'] = i.get('positionAdvantage')
            item['district'] = i.get('district')
            item['companyLabelList'] = ';'.join(i.get('companyLabelList'))
            # item['uid']=i.get('companyId')

            yield item
