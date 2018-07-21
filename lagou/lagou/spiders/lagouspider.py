# -*-coding=utf-8-*-
import json
import re
import datetime
from lagou.items import LagouItem
import scrapy
from lagou.models import DBSession, Jobs
import redis
from lagou import settings
import math


class lagouspider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.years = str(datetime.datetime.now().year)
        self.pool = redis.Redis(host=settings.REDIS_HOST, port=6379, db=settings.REDIS_DB_FIND,decode_responses=True)
        self.cookies = {
            "user_trace_token": "20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644",
            "LGUID": "20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644",
            "_ga": "GA1.2.1514235968.1511234812",
            "LG_LOGIN_USER_ID": "dc82d3e8edcc06f3ee143961873c3ba4ad0d8fe42571bced",
            "index_location_city": "%E5%85%A8%E5%9B%BD",
            "JSESSIONID": "ABAAABAACEBACDGCA1C30CEA6B9D058C206196A1051D923",
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1530191868,1530289763,1530364609,1532137298",
            "_gid": "GA1.2.336535918.1532137304",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1532137332",
            "LGRID": "20180721094213-4a720817-8c87-11e8-a017-525400f775ce",
            "TG-TRACK-CODE": "hpage_code",
        }
        self.url = 'https://www.lagou.com/gongsi/searchPosition.json'
        # self.session = DBSession()
        # self.pool=redis.Redis()

    def start_requests(self):
        # obj = self.session.query(Company).all()
        obj = self.pool.keys()
        for i in obj:
            headers = {
                'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding': 'gzip,deflate,br',
                'Accept-Language': 'zh-CN,zh;q=0.9', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive',
                # 'Content-Length': '89',
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                'Cookie': 'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644;LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644;_ga=GA1.2.1514235968.1511234812;LG_LOGIN_USER_ID=dc82d3e8edcc06f3ee143961873c3ba4ad0d8fe42571bced;index_location_city=%E5%85%A8%E5%9B%BD;JSESSIONID=ABAAABAACEBACDGCA1C30CEA6B9D058C206196A1051D923;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530191868,1530289763,1530364609,1532137298;_gid=GA1.2.336535918.1532137304;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532137332;LGRID=20180721094213-4a720817-8c87-11e8-a017-525400f775ce;TG-TRACK-CODE=hpage_code',
                'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
                'Referer': 'https://www.lagou.com/gongsi/j{}.html'.format(i),
                'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36',
                'X-Anit-Forge-Code': '15954614', 'X-Anit-Forge-Token': '4b88c137-e592-4a33-9e1c-b35c47fd76a4',
                'X-Requested-With': 'XMLHttpRequest'
            }

            data = {
                'companyId': str(i),
                'positionFirstType': '全部',
                'schoolJob': 'false',
                'pageNo': '1',
                'pageSize': '10'
            }
            yield scrapy.http.FormRequest(
                url=self.url,
                headers=headers,
                formdata=data,
                callback=self.parse,
                cookies=self.cookies,
                dont_filter=True,
                meta={'cookiejar':True,
                    'headers': headers, 'data': data}
            )

    def parse(self, response):
        js = json.loads(response.body)
        headers = response.meta['headers']
        data = response.meta['data']
        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = math.ceil(totalCount / 10)
        for i in range(1, int(page) + 1):
            data['pageNo'] = str(i)
            print('page: ', i)
            yield scrapy.FormRequest(url=self.url,
                                     headers=headers,
                                     callback=self.parse_data,
                                     formdata=data,
                                     cookies=self.cookies,
                                     dont_filter=True
                                     )

    def parse_data(self, response):
        js = json.loads(response.body)

        try:
            results = js.get('content').get('data').get('page').get('result')
        except:
            return

        if len(results) == 0:
            print('职位为空')
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

            item['createTime'] = createTime

            s = i.get('salary')
            try:
                if re.search('-', s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')
                    item['salary_low'] = int(s.split('-')[0].replace('k', '000'))
                    item['salary_high'] = int(s.split('-')[1].replace('k', '000'))
                elif re.search('以上', s):
                    if re.findall('K', s):
                        s = s.replace('K', 'k')

                    item['salary_low'] = int(re.findall('(\d+)k', s)[0])
                    item['salary_high'] = int(re.findall('(\d+)k', s)[0])

            except Exception as e:
                print('薪资情况')
                print(i.get('salary'))
                print(e)
            item['workYear'] = i.get('workYear')
            item['education'] = i.get('education')
            item['positionAdvantage'] = i.get('positionAdvantage')
            item['district'] = i.get('district')
            item['companyLabelList'] = ';'.join(i.get('companyLabelList'))
            # item['uid']=i.get('companyId')
            yield item
