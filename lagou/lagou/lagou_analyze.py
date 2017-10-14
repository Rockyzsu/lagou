#-*-coding=utf-8-*-
from models import Jobs,DBSession

def change_data():
    session=DBSession()
    jobs = session.query(Jobs).all()
    #print len(jobs)
    for job in jobs:
        #print job.positionName
        job.salary_high=int(job.salary_high.replace('k','000'))
        job.salary_low=int(job.salary_low.replace('k','000'))
        session.commit()

    session.close()

def analyze():
    session=DBSession()
    ret = session.query(Jobs.salary_low,Jobs.salary_high,Jobs.positionName).order_by(Jobs.salary_high).all()
    salary_low = [i[0] for i in ret]
    for i in salary_low:
        #print i
        pass
    salary_high = [i[1] for i in ret]
    print sum(salary_low)/len(salary_low)
    print sum(salary_high)/len(salary_high)
if __name__ == '__main__':
    analyze()