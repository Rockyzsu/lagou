#-*-coding=utf-8-*-
import json
from lagou.items import LagouItem
import scrapy

class lagouspider(scrapy.Spider):
    name = 'lagou'
    allowed_domains=['lagou.com']
    def __init__(self):
        self.headers =   {
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
               'Referer': 'https://www.lagou.com/gongsi/j917.html',
               }
        self.data = {'companyId': '917',
                'positionFirstType': u'全部',
                'schoolJob': 'False',
                'pageNo': '1',
                'pageSize': '10'}

        self.url='https://www.lagou.com/gongsi/searchPosition.json'

    def start_requests(self):
        self.data = {'companyId': '917',
                'positionFirstType': u'全部',
                'schoolJob': 'False',
                'pageNo': '1',
                'pageSize': '10'}
        yield scrapy.FormRequest(
            url=self.url,
            headers=self.headers,
            formdata=self.data,
            callback=self.parse
        )

    def parse(self, response):
        print 'in parse'
        js = json.loads(response.body)
        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = (totalCount + 10)/10
        for i in range(1,page+1):
            yield scrapy.FormRequest(url=self.url,headers=self.headers,callback=self.parse_data,formdata=self.data)


    def parse_data(self,response):
        js = json.loads(response.body)
        results = js.get('content').get('data').get('page').get('result')
        for i in results:
            item=LagouItem()
            item['companyId'] =i.get('companyId')
            item['positionId'] =i.get('positionId')
            item['jobNature'] =i.get('jobNature')
            item['companyName'] =i.get('companyName')
            item['financeStage'] =i.get('financeStage')
            item['companyFullName'] =i.get('companyFullName')
            item['companySize'] =i.get('companySize')
            item['industryField'] =i.get('industryField')
            item['positionName'] =i.get('positionName')
            item['city'] =i.get('city')
            item['createTime'] =i.get('createTime')
            item['salary'] =i.get('salary')
            item['workYear'] =i.get('workYear')
            item['education'] =i.get('education')
            item['positionAdvantage'] =i.get('positionAdvantage')
            item['district'] =i.get('district')
            item['companyLabelList'] =';'.joint(i.get('companyLabelList'))

            yield item
