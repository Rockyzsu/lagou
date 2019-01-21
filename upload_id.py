# -*-coding=utf-8-*-

# @Time : 2019/1/2 15:44
# @File : upload_id.py
import pymongo
from lagou.models import Jobs, DBSession


def upload_jobid():
    db = pymongo.MongoClient('10.18.6.26', port=27001)
    session = DBSession()
    obj = session.query(Jobs.positionId).all()
    job_id_list = [i[0] for i in obj]
    job_id_set = set(job_id_list)

    ret = db['db_parker']['lagou_jobID'].find({}, {'jobid': 1})
    ret_list = [i.get('jobid') for i in ret]
    ret_list_set = set(ret_list)

    total = job_id_set | ret_list_set
    result = total - ret_list_set
    d = []
    for j in result:
        d.append({'jobid': j})

    for i in d:
        try:
            db['db_parker']['lagou_jobID'].insert(i)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    upload_jobid()
