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
    kws = ['爬虫']
    years = str(datetime.datetime.now().year)

    headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding':
        'gzip,deflate,br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Cache-Control': 'no-cache',
               # 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               'Cookie': 'JSESSIONID=ABAAABAABEEAAJAACF8F22F99AFA35F9EEC28F2D0E46A41;_ga=GA1.2.331323650.1548204973;_gat=1;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548204973;user_trace_token=20190123085612-adf35b62-1ea9-11e9-b744-5254005c3644;LGSID=20190123085612-adf35c69-1ea9-11e9-b744-5254005c3644;PRE_UTM=;PRE_HOST=;PRE_SITE=;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;LGUID=20190123085612-adf35ed5-1ea9-11e9-b744-5254005c3644;_gid=GA1.2.1809874038.1548204973;index_location_city=%E6%B7%B1%E5%9C%B3;TG-TRACK-CODE=index_search;SEARCH_ID=169bf76c08b548f8830967a1968d10ca;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548204985;LGRID=20190123085624-b52a0555-1ea9-11e9-b744-5254005c3644',
               'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
               'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.3;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/71.0.3578.98Safari/537.36',
               'X-Anit-Forge-Code': '0',
               'X-Anit-Forge-Token': 'None',
               'X-Requested-With': 'XMLHttpRequest'
               }
    # 需要定时替换，替换成读取文本或者数据库
    cookies = {
        "JSESSIONID": "ABAAABAABEEAAJAACF8F22F99AFA35F9EEC28F2D0E46A41",
        "_ga": "GA1.2.331323650.1548204973",
        "_gat": "1",
        "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1548204973",
        "user_trace_token": "20190123085612-adf35b62-1ea9-11e9-b744-5254005c3644",
        "LGSID": "20190123085612-adf35c69-1ea9-11e9-b744-5254005c3644",
        "PRE_UTM": "",
        "PRE_HOST": "",
        "PRE_SITE": "",
        "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
        "LGUID": "20190123085612-adf35ed5-1ea9-11e9-b744-5254005c3644",
        "_gid": "GA1.2.1809874038.1548204973",
        "index_location_city": "%E6%B7%B1%E5%9C%B3",
        "TG-TRACK-CODE": "index_search",
        "SEARCH_ID": "169bf76c08b548f8830967a1968d10ca",
        "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1548204985",
        "LGRID": "20190123085624-b52a0555-1ea9-11e9-b744-5254005c3644",
    }

    data = {
        'first': 'false',
        'pn': '1',
        'kd': '',
    }

    URL = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):
        for kw in self.kws:
            self.data['kd'] = kw

            yield scrapy.FormRequest(
                url=self.URL,
                headers=self.headers,
                # cookies=self.cookies,
                formdata=self.data,
                dont_filter=True,
                meta={'page': 1, 'kd': kw}
            )

    def parse(self, response):

        try:
            js_data = json.loads(response.text)
        except Exception as e:
            print(e)
            return
        try:
            job_list = js_data.get('content', {}).get('positionResult', {}).get('result')
        except Exception as e:
            print(e)
            print(response.text)
            return

        if not job_list:
            print(response.text)
            return

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
                    item['salary_low'] = int(
                        s.split('-')[0].replace('k', '000'))
                    item['salary_high'] = int(
                        s.split('-')[1].replace('k', '000'))
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
        total_page = int(math.ceil(
            int(js_data.get('content').get('positionResult').get('totalCount')) / 15))

        if total_page > current_page:
            data = self.data.copy()
            next_page = current_page + 1
            data['pn'] = str(next_page)
            data['kd'] = response.meta['kd']

            yield scrapy.FormRequest(
                url=self.URL,
                headers=self.headers,
                # cookies=self.cookies,
                formdata=data,
                dont_filter=True,
                meta={'page': next_page, 'kd': response.meta['kd']}
            )
