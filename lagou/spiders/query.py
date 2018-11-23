# -*-coding=utf-8-*-

# @Time : 2018/11/22 9:39
# @File : query.py
import datetime
import json
import math
import re

import scrapy
# from scrapy import Spider,Request,FormRequest
from lagou.items import LagouItem


class QuerySpider(scrapy.Spider):
    name = 'query_job'
    kw = '爬虫'
    years = str(datetime.datetime.now().year)

    headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding': 'gzip,deflate,br',
               'Accept-Language': 'zh,en;q=0.9,en-US;q=0.8', 'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               # 'Content-Length': '37',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               # 'Cookie': 'JSESSIONID=ABAAABAAAGFABEF8B7F2F7B6456E459FEF825D0DBB1FAAE;user_trace_token=20181119184953-f8b2ed00-c305-48a2-b797-99ec6c2809a4;_ga=GA1.2.1290529047.1542624594;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542624594;LGUID=20181119184956-da92a9a5-ebe8-11e8-a727-525400f775ce;_gid=GA1.2.41473263.1542781721;index_location_city=%E5%85%A8%E5%9B%BD;X_HTTP_TOKEN=d36294eca3be69f420b943cda015fcc0;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542849275;_gat=1;LGSID=20181122091435-f9b298eb-edf3-11e8-b393-525400f775ce;PRE_UTM=;PRE_HOST=;PRE_SITE=;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;LGRID=20181122091435-f9b29b0a-edf3-11e8-b393-525400f775ce;TG-TRACK-CODE=index_search;SEARCH_ID=cb1a677f4dd148fbbb733e8aeff9578d',
               'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
               'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/67.0.3396.99Safari/537.36',
               'X-Anit-Forge-Code': '0', 'X-Anit-Forge-Token': 'None', 'X-Requested-With': 'XMLHttpRequest'}
    cookies = {
        "JSESSIONID": "ABAAABAAAGFABEF8B7F2F7B6456E459FEF825D0DBB1FAAE",
        "user_trace_token": "20181119184953-f8b2ed00-c305-48a2-b797-99ec6c2809a4",
        "_ga": "GA1.2.1290529047.1542624594",
        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542624594",
        "LGUID": "20181119184956-da92a9a5-ebe8-11e8-a727-525400f775ce",
        "_gid": "GA1.2.41473263.1542781721",
        "index_location_city": "%E5%85%A8%E5%9B%BD",
        "X_HTTP_TOKEN": "d36294eca3be69f420b943cda015fcc0",
        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1542849275",
        "_gat": "1",
        "LGSID": "20181122091435-f9b298eb-edf3-11e8-b393-525400f775ce",
        "PRE_UTM": "",
        "PRE_HOST": "",
        "PRE_SITE": "",
        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
        "LGRID": "20181122091435-f9b29b0a-edf3-11e8-b393-525400f775ce",
        "TG-TRACK-CODE": "index_search",
        "SEARCH_ID": "cb1a677f4dd148fbbb733e8aeff9578d",
    }

    data = {
        'first': 'false',
        'pn': '1',
        'kd': kw,
    }

    URL = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):

        yield scrapy.FormRequest(
            url=self.URL,
            headers=self.headers,
            cookies=self.cookies,
            formdata=self.data,
            dont_filter=True,
            meta={'page': 1}
        )

    def parse(self, response):

        try:
            js_data = json.loads(response.text)
        except Exception as e:
            print(e)
            return

        job_list = js_data.get('content').get('positionResult').get('result')
        for i in job_list:

            item = LagouItem()
            item['companyId'] = i.get('companyId')
            item['positionId'] = i.get('positionId')
            item['jobNature'] = i.get('jobNature')

            item['companyName'] = i.get('companyName')
            if i.get('companyName'):
                item['companyName'] = i.get('companyName')
            else:
                item['companyName'] = i.get('companyShortName')

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

            yield item

        current_page = response.meta['page']
        total_page = int(math.ceil(int(js_data.get('content').get('positionResult').get('totalCount')) / 15))

        if total_page > current_page:
            data = self.data.copy()
            next_page = current_page + 1
            data['pn'] = str(next_page)

            yield scrapy.FormRequest(
                url=self.URL,
                headers=self.headers,
                cookies=self.cookies,
                formdata=data,
                dont_filter=True,
                meta={'page': next_page}
            )
