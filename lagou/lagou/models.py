#-*-coding=utf-8-*-
from sqlalchemy import create_engine,text,func
from sqlalchemy.orm import sessionmaker,relationship
import redis
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime, Integer, Text, INT,ForeignKey,Index
#from mayidaili import useproxy
from sqlalchemy import event
from sqlalchemy import DDL
engine = create_engine('mysql+pymysql://root:123456z@localhost:3306/db_parker?charset=utf8')
DBSession = sessionmaker(bind=engine)
Base = declarative_base()
session = DBSession()

class Jobs(Base):
    __tablename__ = 'tb_jobs'
    id = Column(Integer, primary_key=True)
    companyId = Column(Integer)
    positionId = Column(Integer)
    jobNature = Column(Text)
    companyName = Column(String(160))
    financeStage = Column(String(160))
    companyFullName = Column(String(160))
    companySize = Column(String(160))
    industryField = Column(String(160))
    positionName = Column(String(160),index=True)
    city = Column(String(160))
    createTime = Column(DateTime,index=True)
    salary_low = Column(Integer,index=True)
    salary_high = Column(Integer,index=True)
    workYear = Column(String(160))
    education = Column(String(160))
    positionAdvantage = Column(String(160))
    district = Column(String(160))
    companyLabelList = Column(String(320))

Base.metadata.create_all(engine)