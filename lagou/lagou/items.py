# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    companyId = scrapy.Field()
    positionId = scrapy.Field()
    jobNature = scrapy.Field()
    companyName = scrapy.Field()
    financeStage = scrapy.Field()
    companyFullName = scrapy.Field()
    companySize = scrapy.Field()
    industryField = scrapy.Field()
    positionName = scrapy.Field()
    city = scrapy.Field()
    createTime = scrapy.Field()
    salary_low = scrapy.Field()
    salary_high = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    positionAdvantage = scrapy.Field()
    district = scrapy.Field()
    companyLabelList = scrapy.Field()

