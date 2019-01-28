# -*-coding=utf-8-*-

# @Time : 2019/1/24 8:53
# @File : search_company.py
import datetime

from scrapy import cmdline
cmd='scrapy crawl company -s LOG_FILE=detail-{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
cmdline.execute(cmd.split())