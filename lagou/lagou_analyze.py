#-*-coding=utf-8-*-
from lagou.models import Jobs,DBSession

def change_data():
    session=DBSession()
    jobs = session.query(Jobs).all()
    #print len(jobs)
    for job in jobs:
        #print job.positionName
        job.salary_high=jobs.salary_high
        job.salary_low=job.salary_low
        #session.commit()

    #session.close()

def analyze():
    session=DBSession()
    ret = session.query(Jobs.salary_low,Jobs.salary_high,Jobs.positionName).order_by(Jobs.salary_high).filter(Jobs.companyId==197319).all()
    salary_low = [i[0] for i in ret]
    for i in salary_low:
        #print i
        pass
    salary_high = [i[1] for i in ret]
    print(sum(salary_low)/len(salary_low))
    print(sum(salary_high)/len(salary_high))

def analyze_compay():
    cmpId=451
    session = DBSession()
    ret = session.query(Jobs.salary_low, Jobs.salary_high, Jobs.positionName).filter(Jobs.companyId==cmpId).order_by(Jobs.salary_high).all()
    salary_low = [i[0] for i in ret]
    salary_high = [i[1] for i in ret]
    print(sum(salary_low)/len(salary_low))
    print(sum(salary_high)/len(salary_high))

if __name__ == '__main__':
    analyze_compay()
