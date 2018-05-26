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
        self.pool = redis.Redis(host='raspberrypi', port=6379, db=2)
        self.cookies = {"user_trace_token": "20160612223035-3a02d006-30aa-11e6-a343-5254005c3644",
                        "LGUID": "20160612223035-3a02d566-30aa-11e6-a343-5254005c3644",
                        "SEARCH_ID": "08c78425fe834aad93ccda9367e90b39",
                        "JSESSIONID": "ABAAABAACDBAAIABC4729F0A9CEC95D283FC7071EF87E1E",
                        "PRE_UTM": "",
                        "PRE_HOST": "",
                        "PRE_SITE": "",
                        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
                        "_putrc": "DFAF58A586D854B0",
                        "login": "true",
                        "unick": "%E9%99%88%E9%94%A6%E4%BC%9F",
                        "showExpriedIndex": "1",
                        "showExpriedCompanyHome": "1",
                        "showExpriedMyPublish": "1",
                        "hasDeliver": "138",
                        "TG-TRACK-CODE": "index_company",
                        "index_location_city": "%E6%B7%B1%E5%9C%B3",
                        "_gat": "1",
                        "_gid": "GA1.2.1667060466.1509002344",
                        "_ga": "GA1.2.499625224.1465741835",
                        "LGSID": "20171027125724-52ba86b9-bad3-11e7-a9d9-525400f775ce",
                        "LGRID": "20171027132206-c5e392f3-bad6-11e7-a9dc-525400f775ce",
                        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1507978370,1508072067,1509002344,1509080246",
                        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1509081728"}
        self.url = 'https://www.lagou.com/gongsi/searchPosition.json'
        # self.session = DBSession()
        #self.pool=redis.Redis()

    def start_requests(self):
        #obj = self.session.query(Company).all()
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
        js = json.loads(response.body)
        headers = response.meta['headers']
        data = response.meta['data']
        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = (totalCount + 10) / 10
        for i in range(1, page + 1):
            data['pageNo'] = str(i)
            print 'page: ', i
            yield scrapy.FormRequest(url=self.url,
                                     headers=headers,
                                     callback=self.parse_data,
                                     formdata=data,
                                     cookies=self.cookies, dont_filter=True)

    def parse_data(self, response):
        js = json.loads(response.body)

        try:
            results = js.get('content').get('data').get('page').get('result')
        except:
            return

        if not results:
            print 'empty'
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
            createTime= i.get('createTime')
            try:
                if not re.search('2017',createTime):
                    createTime=datetime.datetime.now().strftime('%Y-%m-%d') +' '+ createTime

            except Exception,e:
                print e
                print createTime

            item['createTime'] = createTime

            s = i.get('salary')
            try:
                if re.search('-',s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')
                    item['salary_low'] = int(s.split('-')[0].replace('k', '000'))
                    item['salary_high'] = int(s.split('-')[1].replace('k', '000'))
                elif re.search(u'以上',s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')

                    item['salary_low'] = int(re.findall('(\d+)k',s)[0])
                    item['salary_high'] = int(re.findall('(\d+)k',s)[0])



            except Exception, e:
                print 'its salary'
                print i.get('salary')
                print e
            item['workYear'] = i.get('workYear')
            item['education'] = i.get('education')
            item['positionAdvantage'] = i.get('positionAdvantage')
            item['district'] = i.get('district')
            item['companyLabelList'] = ';'.join(i.get('companyLabelList'))
            #item['uid']=i.get('companyId')

            yield item
