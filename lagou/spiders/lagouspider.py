# -*-coding=utf-8-*-
import json
import re
import datetime
from lagou.items import LagouItem
import scrapy
import redis
import pymongo
from lagou import config
import math


# 获取一个公司的所有职位
class lagouspider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    doc = pymongo.MongoClient('10.18.6.26', port=27001)['db_parker']['lagou_company']

    years = str(datetime.datetime.now().year)
    cookies = {
        "JSESSIONID": "ABAAABAAAGFABEF8B7F2F7B6456E459FEF825D0DBB1FAAE",
        "user_trace_token": "20181119184953-f8b2ed00-c305-48a2-b797-99ec6c2809a4",
        "_ga": "GA1.2.1290529047.1542624594",
        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542624594",
        "LGUID": "20181119184956-da92a9a5-ebe8-11e8-a727-525400f775ce",
        "_gid": "GA1.2.41473263.1542781721",
        "index_location_city": "%E5%85%A8%E5%9B%BD",
        "TG-TRACK-CODE": "index_company",
        "_gat": "1",
        "LGSID": "20181121153948-9fcb9991-ed60-11e8-8aa5-5254005c3644",
        "PRE_UTM": "",
        "PRE_HOST": "",
        "PRE_SITE": "https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F215-0-0-0",
        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F50587.html",
        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542785997",
        "LGRID": "20181121153956-a43ffc34-ed60-11e8-b195-525400f775ce",
    }
    url = 'https://www.lagou.com/gongsi/searchPosition.json'

    def start_requests(self):
        ret = self.doc.find({'crawl_status': {'$exists': False}})

        for i in ret:
            company_id = i.get('companyId')
            headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding': 'gzip,deflate,br',
                       'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8', 'Cache-Control': 'no-cache',
                       'Connection': 'keep-alive',
                       # 'Content-Length': '89',
                       'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                       # 'Cookie': 'JSESSIONID=ABAAABAAAGFABEF8B7F2F7B6456E459FEF825D0DBB1FAAE;user_trace_token=20181119184953-f8b2ed00-c305-48a2-b797-99ec6c2809a4;_ga=GA1.2.1290529047.1542624594;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542624594;LGUID=20181119184956-da92a9a5-ebe8-11e8-a727-525400f775ce;_gid=GA1.2.41473263.1542781721;index_location_city=%E5%85%A8%E5%9B%BD;TG-TRACK-CODE=index_company;_gat=1;LGSID=20181121153948-9fcb9991-ed60-11e8-8aa5-5254005c3644;PRE_UTM=;PRE_HOST=;PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F215-0-0-0;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fgongsi%2F50587.html;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542785997;LGRID=20181121153956-a43ffc34-ed60-11e8-b195-525400f775ce',
                       'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
                       'Referer': 'https://www.lagou.com/gongsi/j{}.html'.format(company_id),
                       'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
                       # 'X-Anit-Forge-Code': '42167373', 'X-Anit-Forge-Token': 'f4d40bfe-f114-4946-afb3-f1e51152c93d',
                       'X-Requested-With': 'XMLHttpRequest'
                       }

            data = {
                'companyId': str(company_id),
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
                meta={'cookiejar': True, 'companyid': company_id,
                      'headers': headers, 'data': data},
            )

    def parse(self, response):
        try:
            js = json.loads(response.body)
        except Exception as e:
            print(e)
            return

        headers = response.meta['headers']
        data = response.meta['data']
        comanpy_id = response.meta['companyid']

        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = math.ceil(totalCount / 10)

        self.doc.update({'companyId': comanpy_id}, {'$set': {'crawl_status': 1}})

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
        try:
            js = json.loads(response.body)
        except Exception as e:
            print(e)
            return

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
