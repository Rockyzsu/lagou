# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from lagou.models import Jobs, DBSession,JobDetails
from lagou.items import LagouItem, CompanyItem, JobDetailsItem
import redis
from sqlalchemy import and_
from lagou import config
from lagou import settings


class LagouPipeline(object):
    def __init__(self):
        self.session = DBSession()
        self.pool = redis.Redis(host=settings.REDIS_HOST_FIND, port=6379, db=settings.REDIS_DB_FIND)

    def process_item(self, item, spider):
        if isinstance(item, LagouItem):

            if self.session.query(Jobs).filter(Jobs.positionId == item['positionId'],
                                               Jobs.companyId == item['companyId']).first():
                return item
            else:
                obj = Jobs(
                    companyId=item['companyId'],
                    positionId=item['positionId'],
                    jobNature=item['jobNature'],
                    companyName=item['companyName'],
                    financeStage=item['financeStage'],
                    companyFullName=item['companyFullName'],
                    companySize=item['companySize'],
                    industryField=item['industryField'],
                    positionName=item['positionName'],
                    city=item['city'],
                    createTime=item['createTime'],
                    salary_low=item['salary_low'],
                    salary_high=item['salary_high'],
                    workYear=item['workYear'],
                    education=item['education'],
                    positionAdvantage=item['positionAdvantage'],
                    district=item['district'],
                    # uid=item['uid'],
                    companyLabelList=item['companyLabelList'],
                )
                self.session.add(obj)
                try:
                    self.session.commit()
                except Exception as e:
                    print(e)
                    self.session.rollback()

        elif isinstance(item, CompanyItem):
            # 公司信息存入mysql数据库
            '''
            obj=Company(
                companyId=item['companyId'],
                companyName=item['companyFullName']
            )
            self.session.add(obj)
            try:
                self.session.commit()
            except Exception, e:
                print e
                self.session.rollback()
            '''

            # 公司的数据存入redis
            self.pool.set(item['companyId'], item['companyFullName'])

        elif isinstance(item, JobDetailsItem):
            obj = JobDetails(
                positionId=item['positionId'],
                advantage=item['advantage'],
                description=item['description'],
                address=item['address'],
            )
            self.session.add(obj)
            try:
                self.session.commit()
            except Exception as e:
                print(e)
                self.session.rollback()
        return item
