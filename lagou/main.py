# -*-coding=utf-8-*-
from scrapy import cmdline

cmd='scrapy crawl job_details'
# cmd='scrapy crawl lagou -s LOG_FILE=spider3.log'
# cmd='scrapy crawl company -s LOG_FILE=spider.log'
# cmd = 'scrapy crawl job_details'
cmdline.execute(cmd.split())
