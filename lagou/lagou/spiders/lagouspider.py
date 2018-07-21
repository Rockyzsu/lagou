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
        self.pool = redis.Redis(host=settings.REDIS_HOST, port=6379, db=settings.REDIS_DB_FIND)
        self.cookies = {
            "_ga": "GA1.2.83307641.1530287182",
            "user_trace_token": "20180629234623-92fa9b1e-7bb3-11e8-9775-5254005c3644",
            "LGUID": "20180629234623-92fa9eb7-7bb3-11e8-9775-5254005c3644",
            "index_location_city": "%E5%85%A8%E5%9B%BD",
            "JSESSIONID": "ABAAABAACBHABBI4C80036F8C017CE0A5AFB58686174931",
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1530287183,1531805505",
            "TG-TRACK-CODE": "index_search",
            "_gid": "GA1.2.1182757649.1532098646",
            "SEARCH_ID": "df49e5d9a1f843ae8cb7b21a8025b56a",
            "_gat": "1",
            "LGSID": "20180720235410-245d6175-8c35-11e8-9ff4-525400f775ce",
            "PRE_UTM": "",
            "PRE_HOST": "",
            "PRE_SITE": "https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2596%25B0%25E5%259B%25BD%25E9%2583%25BD%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D",
            "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F17433.html",
            "LGRID": "20180720235502-4351cae3-8c35-11e8-9e4d-5254005c3644",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1532102102"}
        self.url = 'https://www.lagou.com/gongsi/searchPosition.json'
        # self.session = DBSession()
        # self.pool=redis.Redis()

    def start_requests(self):
        # obj = self.session.query(Company).all()
        obj = self.pool.keys()
        for i in obj:
            headers = {
                # 'Accept': 'application/json,text/javascript,*/*;q=0.01',
                #        'Accept-Encoding': 'gzip,deflate,br',
                       'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8', 'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       # 'Content-Length': '89',
                       'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                       # 'Cookie': '_ga=GA1.2.83307641.1530287182;user_trace_token=20180629234623-92fa9b1e-7bb3-11e8-9775-5254005c3644;LGUID=20180629234623-92fa9eb7-7bb3-11e8-9775-5254005c3644;index_location_city=%E5%85%A8%E5%9B%BD;JSESSIONID=ABAAABAACBHABBI4C80036F8C017CE0A5AFB58686174931;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530287183,1531805505;TG-TRACK-CODE=index_search;_gid=GA1.2.1182757649.1532098646;SEARCH_ID=df49e5d9a1f843ae8cb7b21a8025b56a;_gat=1;LGSID=20180720235410-245d6175-8c35-11e8-9ff4-525400f775ce;PRE_UTM=;PRE_HOST=;PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2596%25B0%25E5%259B%25BD%25E9%2583%25BD%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F17433.html;LGRID=20180720235502-4351cae3-8c35-11e8-9e4d-5254005c3644;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532102102',
                       'Host': 'www.lagou.com',
                       'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
                       # 'Referer': 'https://www.lagou.com/gongsi/j32687.html',
                       'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
                       # 'X-Anit-Forge-Code': '86010399', 'X-Anit-Forge-Token': 'abb50957-4555-4f33-9bad-6a0359261858',
                       # 'X-Requested-With': 'XMLHttpRequest',
                       'Referer': 'https://www.lagou.com/gongsi/j%s.html' % i,
                       }

            data = {
                'companyId': str(i),
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
                meta={'cookiejar': True,
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
