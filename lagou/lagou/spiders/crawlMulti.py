from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import Rule
from scrapy.spider import CrawlSpider
from scrapy import Request
class AutoCrawl(CrawlSpider):
    name = "xitek"
    allowed_domains=['photo.xitek.com']
    start_urls=['http://photo.xitek.com']
    rules = [Rule(LinkExtractor(allow=['/\d{6}']),'parse_link')]

    def parse_link(self, response):
        url=response.url
        print url
        yield Request(url=url,callback='parse_link')
