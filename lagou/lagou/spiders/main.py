__author__ = 'xda'
import scrapy
import collections
from lagou.items import LagouItem
import codecs
class KeywordSpider(scrapy.Spider):
    name = 'lagou'
    allowed_donmains=[' lagou.com']
    start_urls=['http://www.lagou.com/']

    def parse(self, response):
        print "\n"*5
        f=codecs.open("kw.txt",'w','utf-8')
        print response.xpath("//title/text()").extract()[0]
        #response.xpath('//h2')
        tech_menu=response.xpath('//div[contains(@class,"menu_box")]')[0]
        tech_detail=tech_menu.xpath('.//div[contains(@class,"menu_sub dn")]/dl')
        #sub_tech=tech_menu.xpath('a/text()').extract()
        #item=collections.defaultdict(list)

        for i in tech_detail:
            job= i.xpath('.//a/text()').extract()
            for j in job:
                print j
                #item=LagouItem()
                item=j
                f.write(item+'\n')
                yield item


        '''
        for i in menu_sub:
            print i
        '''
        f.close()
        print "Done"
        print "\n"*5
        '''
        dl=menu_sub[0].xpath('dl')
        for i in dl:
        '''
