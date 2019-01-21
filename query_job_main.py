# -*-coding=utf-8-*-

# @Time : 2019/1/2 15:14
# @File : query_job_main.py
import datetime
from scrapy import cmdline

# cmd='scrapy crawl query_job -s LOG_FILE=query{}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d"))
cmd='scrapy crawl query_job'
cmdline.execute(cmd.split())