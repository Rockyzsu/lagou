# -*-coding=utf-8-*-
from scrapy import cmdline

# cmd='scrapy crawl company'
# cmd='scrapy crawl company -s LOG_FILE=spider.log'
cmd = 'scrapy crawl lagou'
cmdline.execute(cmd.split())
