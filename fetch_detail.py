# -*-coding=utf-8-*-

# @Time : 2019/1/2 15:15
# @File : fetch_detail.py
import datetime
from scrapy import cmdline

cmd='scrapy crawl job_details -s LOG_FILE=detail-{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
cmdline.execute(cmd.split())