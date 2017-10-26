# -*-coding=utf-8-*-
import json

import re
from lagou.items import LagouItem
import scrapy


class lagouspider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']

    def __init__(self):
        self.companyid = 917

        self.cookies = {
            "user_trace_token": "20160612223035-3a02d006-30aa-11e6-a343-5254005c3644",
            "LGUID": "20160612223035-3a02d566-30aa-11e6-a343-5254005c3644",
            "index_location_city": "%E6%B7%B1%E5%9C%B3",
            "JSESSIONID": "ABAAABAACDBAAIA2AF78F3B190ED86CE3AD74D3F50F274F",
            "PRE_UTM": "",
            "PRE_HOST": "",
            "PRE_SITE": "",
            "PRE_LAND": "https%3A%2F%2Fwww.lagou.com%2F",
            "SEARCH_ID": "7dbfb6a19b0145138d38cef38a59c176",
            "TG-TRACK-CODE": "hpage_code",
            "_gid": "GA1.2.1667060466.1509002344",
            "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1507809365,1507978370,1508072067,1509002344",
            "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1509003561",
            "_ga": "GA1.2.499625224.1465741835",
            "LGSID": "20171026151903-f204f6c9-ba1d-11e7-9626-5254005c3644",
            "LGRID": "20171026153920-c755348b-ba20-11e7-a914-525400f775ce"
        }

        self.headers = {
            'Origin': 'https://www.lagou.com', 'Content-Length': '87',
            'Accept-Language': 'zh,en;q=0.8,en-US;q=0.6',
            'Accept-Encoding': 'gzip, deflate, br', 'X-Anit-Forge-Code': '58621840',
            'X-Requested-With': 'XMLHttpRequest',
            'X-Anit-Forge-Token': '74a55bb9-e651-47da-8f1e-4f6df2f97b31',
            'Host': 'www.lagou.com', 'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache', 'Cache-Control': 'no-cache',
            'Referer': 'https://www.lagou.com/gongsi/j{}.html'.format(self.companyid),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        self.data = {'companyId': str(self.companyid),
                     'positionFirstType': u'全部',
                     'schoolJob': 'false',
                     'pageNo': '1',
                     'pageSize': '10'}

        self.url = 'https://www.lagou.com/gongsi/searchPosition.json'

    def start_requests(self):
        yield scrapy.FormRequest(
            url=self.url,
            headers=self.headers,
            formdata=self.data,
            callback=self.parse,
            #cookies=self.cookies
        )

    def parse(self, response):
        print 'in parse'
        js = json.loads(response.body)
        totalCount = int(js.get('content').get('data').get('page').get('totalCount'))
        page = (totalCount + 10) / 10
        for i in range(1, page + 1):
            self.data['pageNo'] = str(i)
            print 'page: ', i
            yield scrapy.FormRequest(url=self.url, headers=self.headers, callback=self.parse_data,
                                          formdata=self.data, cookies=self.cookies, dont_filter=True)

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
            item['createTime'] = i.get('createTime')
            try:
                s = i.get('salary')
                if re.findall('K', s):
                    s = s.replace('K', 'k')
                item['salary_low'] = int(s.split('-')[0].replace('k', '000'))
                item['salary_high'] = int(s.split('-')[1].replace('k', '000'))
            except Exception, e:
                print e
            item['workYear'] = i.get('workYear')
            item['education'] = i.get('education')
            item['positionAdvantage'] = i.get('positionAdvantage')
            item['district'] = i.get('district')
            item['companyLabelList'] = ';'.join(i.get('companyLabelList'))
            yield item
