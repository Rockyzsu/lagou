# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

from lagou.models import Jobs, DBSession,JobDetails
from lagou.items import LagouItem, CompanyItem, JobDetailsItem
import redis
from sqlalchemy import and_
from lagou import config
from lagou import settings
import pymongo
from scrapy.exceptions import DropItem
from lagou.settings import MONGODB
class LagouPipeline(object):

    def __init__(self):
        self.session = DBSession()
        self.db = pymongo.MongoClient(MONGODB,port=27001)
        self.company_id_doc=self.db['db_parker']['lagou_company_id']


    def process_item(self, item, spider):

        # 职位基本信息，列表形式
        if isinstance(item, LagouItem):

            ret = self.session.query(Jobs).filter(Jobs.positionId == item['positionId'],
                                            Jobs.companyId == item['companyId']).first()
            if ret:
                ret.createTime=item['createTime']
                ret.updated=datetime.datetime.now()

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
            # 公司的数据存入mongo
            d={'company_id':item['companyId'], 'company_name':item['companyFullName']}
            try:
                self.company_id_doc.insert(d)
            except Exception as e:
                print(e)
                raise DropItem(item)
            else:
                return item

        elif isinstance(item, JobDetailsItem):
            obj = JobDetails(
                positionId=item['positionId'],
                advantage=item['advantage'],
                description=item['description'],
                address=item['address'],
                jobTitle=item['jobTitle'],
                companyName=item['companyName'],

            )
            self.session.add(obj)
            try:
                self.session.commit()
            except Exception as e:
                print(e)
                self.session.rollback()

            try:
                self.db['db_parker']['lagou_jobID'].update({'jobid':item['positionId']},{'$set':{'status':1}})
            except Exception as e:
                print(e)

        return item
