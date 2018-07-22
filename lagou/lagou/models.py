#-*-coding=utf-8-*-
from sqlalchemy import create_engine,text,func
from sqlalchemy.orm import sessionmaker,relationship
import redis
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Text,ForeignKey,Index
#from mayidaili import useproxy
from sqlalchemy import event
from sqlalchemy import DDL
from lagou import settings
engine = create_engine('mysql+pymysql://{}:{}@{}:3306/db_rocky?charset=utf8'.format(settings.MYSQL_USER,settings.MYSQL_PASSWD,settings.MYSQL_HOST))
DBSession = sessionmaker(bind=engine)
Base = declarative_base()

class Jobs(Base):
    __tablename__ = 'tb_jobs'
    id = Column(Integer, primary_key=True)
    companyId = Column(Integer)
    positionId = Column(Integer,index=True)
    jobNature = Column(Text)
    companyName = Column(String(160))
    financeStage = Column(String(160))
    companyFullName = Column(String(160))
    companySize = Column(String(160))
    industryField = Column(String(160))
    positionName = Column(String(160),index=True)
    city = Column(String(160),index=True)
    createTime = Column(String(80),index=True)
    salary_low = Column(Integer,index=True)
    salary_high = Column(Integer,index=True)
    workYear = Column(String(160))
    education = Column(String(160))
    positionAdvantage = Column(String(160))
    district = Column(String(160))
    companyLabelList = Column(String(320))
    updated = Column(DateTime,default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #uid= Column(Integer,ForeignKey('tb_company.companyId'))

'''
class Company(Base):
    __tablename__ = 'tb_company'

    #id = Column(Integer)
    companyId = Column(Integer,index=True,primary_key=True)
    companyName = Column(String(200))
    jobs = relationship('Jobs',backref='jobinfo')
'''
class JobDetails(Base):

    __tablename__ = 'tb_jobs_details'
    id = Column(Integer, primary_key=True,autoincrement=True)
    positionId = Column(String(30), index=True)
    advantage=Column(Text)
    description=Column(Text)
    address=Column(Text)

    updated = Column(DateTime, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

Base.metadata.create_all(engine)