# -*-coding=utf-8-*-
import re

import scrapy
import redis
from lagou.models import Jobs, DBSession
from lagou.items import JobDetailsItem


class JobDetails(scrapy.Spider):
    name = 'job_details'
    r = redis.StrictRedis('localhost', port=6379, db=7, decode_responses=True)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644;LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644;_ga=GA1.2.1514235968.1511234812;LG_LOGIN_USER_ID=dc82d3e8edcc06f3ee143961873c3ba4ad0d8fe42571bced;index_location_city=%E5%85%A8%E5%9B%BD;_gid=GA1.2.336535918.1532137304;SEARCH_ID=1c44f6e009f74385b452140b11a83391;JSESSIONID=ABAAABAACBHABBIFF83D5E8AA75192334A95E9C120BC2F6;_gat=1;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1530289763,1530364609,1532137298,1532185061;LGSID=20180721225742-6b80a8ff-8cf6-11e8-9e4e-5254005c3644;PRE_UTM=;PRE_HOST=;PRE_SITE=;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;TG-TRACK-CODE=hpage_code;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1532185151;LGRID=20180721225912-a1099e26-8cf6-11e8-9e4e-5254005c3644',
        'Host': 'www.lagou.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36'}

    def start_requests(self):
        jobid = self.r.lpop('lagou_jobID')

        while jobid:
            url = 'https://www.lagou.com/jobs/{}.html'.format(jobid)
            yield scrapy.Request(url=url, headers=self.headers)
            jobid = self.r.lpop('lagou_jobID')

    def parse(self, response):
        item = JobDetailsItem()
        advantage = response.xpath('//dd[@class="job-advantage"]//p/text()').extract_first()
        if advantage:
            advantage = advantage.strip()
        positionId = re.findall('https://www.lagou.com/jobs/(.*?).html', response.url)[0]
        description = response.xpath('//dd[@class="job_bt"]/div')[0].xpath('string(.)').extract_first()
        if description:
            description = description.strip()

        address = response.xpath('//div[@class="work_addr"]')[0].xpath('string(.)').extract_first()
        if address:
            address = address.strip()

        item['positionId'] = positionId
        item['description'] = description
        item['advantage'] = advantage
        item['address'] = address
        yield item


def upload_jobid():
    r = redis.StrictRedis('localhost', port=6379, db=7, decode_responses=True)
    session = DBSession()
    obj = session.query(Jobs.positionId).all()[:50]
    for i in obj:
        r.lpush('lagou_jobID', i[0])


# upload_jobid()
