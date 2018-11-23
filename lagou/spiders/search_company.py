# -*-coding:utf-8
import pymongo
from lagou.models import Jobs, DBSession
import requests
import redis
import pymysql
from lagou import settings
from lagou import config
# 根据招聘的职位找公司名
def get_redis(db_num):
    pool = redis.Redis(host=config.redis_host, port=6379, db=db_num,decode_responses=True)
    return pool

# job_redis = get_redis(5)

def get_mysql_conn(db):
    conn = pymysql.connect(settings.MYSQL_HOST, settings.MYSQL_USER, settings.MYSQL_PASSWD, db, charset='utf8')
    return conn


def find_positionName():
    conn = get_mysql_conn('db_rocky')
    # 实际这一句mysql语句已经去重了
    cmd = 'select `positionName`,count(*) as count from tb_jobs group by `positionName` order by count desc'
    cursor = conn.cursor()
    cursor.execute(cmd)
    ret = cursor.fetchall()
    count=0
    for i in ret:
        name = i[0].strip()
        if len(name) == 0:
            continue
        # 必要的时候再去把所有职位入栈
        print('Count : ',count)
        enqueue_redis(name.strip() )
        count+=1

def comsure_get():
    while 1:
        try:
            name = job_redis.spop('lagou_set')
        except Exception as e:
            print(e)
            break

        if name is None:
            print('队列为空')
            break
        else:
            print('Job : ',name)
            search_company(name)

    # unique_job = job_redis.smembers('lagou')
    # job_redis.lpush('lagou_list',list(unique_job))

# 职位名称入队列
def enqueue_redis(name):
    try:
        job_redis.sadd('lagou_set',name)
    except Exception as e:
        print(e)



def distributed_crawl():
    while 1:
        try:
            name = job_redis.blpop('lagou')
            if name is None:
                pass
        except Exception as e:
            print(e)
            break
def search_company(name):
    company_redis = get_redis(6)
    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
    print(url)
    headers = {
        'Origin': 'https://www.lagou.com',
        'Accept-Encoding': 'gzip,deflate,br', 'X-Anit-Forge-Code': '0',
        'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': 'None',
        'Host': 'www.lagou.com', 'Accept': 'application/json,text/javascript,*/*;q=0.01',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36',
        'Connection': 'keep-alive',
        'Cookie': 'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644; LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644; _ga=GA1.2.1514235968.1511234812; LG_LOGIN_USER_ID=87df3eb128a51a99595ac0e041c1ec2ae82012416f63916c; JSESSIONID=ABAAABAAAGFABEFAFF540316A9C596C7C95AEC19F8FC61A; _gid=GA1.2.1275640327.1528596573; LGSID=20180610100945-5873e300-6c53-11e8-9952-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527327829,1527601928,1528356179,1528596582; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=9b3b4ca5be85f2540679671acec8948f; index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=c51fde656e4c40c5b9afb164ccc525a8; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528596864; LGRID=20180610101453-0faf08ec-6c54-11e8-9952-525400f775ce',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    page = 1
    break_out = False
    while 1:
        print('page {}'.format(page))
        data = {
            'first': 'false',
            'pn': '1',
            'kd': name
        }
        data['pn'] = str(page)
        r = requests.post(url, headers=headers, data=data)
        try:
            js = r.json()
        except Exception as e:
            print(e)
            break
        # print js.get('content')

        if js.get('content').get('positionResult').get('totalCount') / 15 < (page + 3):
            # if js.get('content').get('resultSize')==0:
            break
        if break_out:
            break

        for i in js.get('content').get('positionResult').get('result'):
            fullname = i.get('companyFullName')
            companyId = i.get('companyId')
            if companyId is None:
                break_out = True
            try:
                company_redis.set(companyId, fullname)
            except Exception as e:
                print(e)

        if js.get('content').get('positionResult').get('result') is None:
            break
        page += 1
#
def upload_jobid():
    db=pymongo.MongoClient('10.18.6.26',port=27001)
    session = DBSession()
    obj = session.query(Jobs.positionId).order_by(Jobs.createTime).all()
    job_id_list = [i[0] for i in obj]
    ret = list(db['db_parker']['lagou_jobID'].find({}))
    ret_list = [i.get('jobid') for i in ret]
    # for i in ret_list:
    # count=0
    for j in job_id_list:
        if j not in ret_list:
            try:
                print(j)
                db['db_parker']['lagou_jobID'].insert({'jobid':j})
            except Exception as e:
                print(e)

if __name__=='__main__':
    # find_positionName()
    # comsure_get()
    upload_jobid()