# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from models import Jobs,DBSession

class LagouPipeline(object):
    def __init__(self):
        self.session=DBSession()

    def process_item(self, item, spider):
        obj = Jobs(
        companyId = item['companyId'],
        positionId = item['positionId'],
        jobNature = item['jobNature'],
        companyName = item['companyName'],
        financeStage = item['financeStage'],
        companyFullName = item['companyFullName'],
        companySize = item['companySize'],
        industryField = item['industryField'],
        positionName = item['positionName'],
        city = item['city'],
        createTime = item['createTime'],
        salary_low = item['salary_low'],
        salary_high = item['salary_high'],
        workYear = item['workYear'],
        education = item['education'],
        positionAdvantage = item['positionAdvantage'],
        district = item['district'],
        companyLabelList = item['companyLabelList'],
        )

        self.session.add(obj)
        try:
            self.session.commit()
        except:
            self.session.rollback()

        self.session.close()

        return item
