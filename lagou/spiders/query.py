# -*-coding=utf-8-*-

# @Time : 2018/11/22 9:39
# @File : query.py
import datetime
import json
import math
import re
import requests

import scrapy
# from scrapy import Spider,Request,FormRequest
from lagou.items import LagouItem
import urllib.parse


# 需要自动更新cookie

class QuerySpider(scrapy.Spider):
    name = 'query_job'
    kws = ['爬虫', '数据挖掘', '数据分析']
    years = str(datetime.datetime.now().year)
    headers = {'Accept': 'application/json,text/javascript,*/*;q=0.01', 'Accept-Encoding':
        'gzip,deflate,br',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Cache-Control': 'no-cache',
               # 'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
               # 'Cookie':'JSESSIONID=ABAAABAABEEAAJAACF8F22F99AFA35F9EEC28F2D0E46A41; _ga=GA1.2.331323650.1548204973; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548204973; user_trace_token=20190123085612-adf35b62-1ea9-11e9-b744-5254005c3644; LGUID=20190123085612-adf35ed5-1ea9-11e9-b744-5254005c3644; _gid=GA1.2.1809874038.1548204973; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216878b38c2b1f2-0fc8f58d18d562-671b197c-2073600-16878b38c2c8b4%22%2C%22%24device_id%22%3A%2216878b38c2b1f2-0fc8f58d18d562-671b197c-2073600-16878b38c2c8b4%22%7D; LG_LOGIN_USER_ID=d10beafda0ba442e7fbc48af7d2de3524a3f4b0e75614abd; _putrc=DFAF58A586D854B0; login=true; unick=%E9%99%88%E9%94%A6%E4%BC%9F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=209; index_location_city=%E5%85%A8%E5%9B%BD; _gat=1; LGSID=20190124085649-ee0c962a-1f72-11e9-977f-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; gate_login_token=838ff604b9266ba08eb2346edd893d244d1e798ed5b7f887; X_MIDDLE_TOKEN=2b8deed60f86f33374c17e46b4bbc6ae; SEARCH_ID=f8b50adc016c42af812c4f9f304b0223; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1548291536; LGRID=20190124085855-399ee8ad-1f73-11e9-b74c-5254005c3644; TG-TRACK-CODE=search_code',
               'Host': 'www.lagou.com', 'Origin': 'https://www.lagou.com', 'Pragma': 'no-cache',
               'Referer': 'https://www.lagou.com/jobs/list_{}?labelWords=&fromSearch=true&suginput=',
               'User-Agent': 'Mozilla/5.0(WindowsNT6.3;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/71.0.3578.98Safari/537.36',
               'X-Anit-Forge-Code': '0',
               'X-Anit-Forge-Token': 'None',
               'X-Requested-With': 'XMLHttpRequest'
               }
    # 需要定时替换，替换成读取文本或者数据库

    data = {
        'first': 'false',
        'pn': '1',
        'kd': '',
    }

    URL = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):
        cookies = self.update_cookies_redis()
        for kd in self.kws:
            word = urllib.parse.unquote(kd)
            self.headers['Referer'] = self.headers['Referer'].format(word)
            self.data['kd'] = kd

            yield scrapy.FormRequest(
                url=self.URL,
                headers=self.headers,
                cookies=cookies,
                formdata=self.data,
                dont_filter=True,
                meta={'page': 1, 'kd': kd, 'cookiejar': True}
            )

    def parse(self, response):
        kd = response.meta['kd']
        current_page = response.meta['page']

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
            if js_data.get('msg') == '您操作太频繁,请稍后再访问':
                cookies = self.update_cookies()
                print('更新cookiejar')
                print(cookies)
                yield scrapy.FormRequest(
                    url=self.URL,
                    headers=self.headers,
                    cookies=cookies,
                    formdata=self.data,
                    dont_filter=True,
                    meta={'page': current_page, 'kd': kd, 'cookiejar': True}
                )

            return
            # return

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

        total_page = int(math.ceil(
            int(js_data.get('content').get('positionResult').get('totalCount')) / 15))

        if total_page > current_page:
            data = self.data.copy()
            next_page = current_page + 1
            data['pn'] = str(next_page)
            data['kd'] = kd
            word = urllib.parse.unquote(kd)
            self.headers['Referer'] = self.headers['Referer'].format(word)
            yield scrapy.FormRequest(
                url=self.URL,
                headers=self.headers,
                # cookies=self.cookies,
                formdata=data,
                dont_filter=True,
                meta={'page': next_page, 'kd': kd, 'cookiejar': True}
            )

    def update_cookies(self):
        headers = {'Host': 'www.lagou.com',
                   'Referer': 'https://www.lagou.com/',
                   'Upgrade-Insecure-Requests': '1',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        url = 'https://www.lagou.com/'
        r = requests.get(url, headers)
        # print(r.status_code)
        # print(r.text)
        # print(r.cookies['JSESSIONID'])
        return dict(r.cookies)

    def update_cookies_redis(self):
