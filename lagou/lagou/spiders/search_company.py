#-*-coding:utf-8
import requests
import redis
import MySQLdb
from lagou.settings import REDIS_HOST,MYSQL_HOST
pool = redis.Redis(host=REDIS_HOST,port=6379,db=3)
def get_mysql_conn(db):


    conn = MySQLdb.connect(MYSQL_HOST, 'rocky', '123456z', db, charset='utf8')

    return conn

def find_positionName():
	conn = get_mysql_conn('db_rocky')
	cmd = 'select `positionName`,count(*) as count from db_rocky.tb_jobs group by `positionName` order by count desc limit 20,20;'
	cursor = conn.cursor()
	cursor.execute(cmd)
	ret = cursor.fetchall()
	for i in ret:
		name= i[0].strip()
		if len(name)<=0:
			continue
		search(name)

def search(name):
		url = r'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'
		print url
		headers = {'Origin': 'https://www.lagou.com', 
		'Content-Length': '38', 'Accept-Language': 'zh-CN,zh;q=0.9', 
		'Accept-Encoding': 'gzip,deflate,br', 'X-Anit-Forge-Code': '0', 
		'X-Requested-With': 'XMLHttpRequest', 'X-Anit-Forge-Token': 'None', 
		'Host': 'www.lagou.com', 'Accept': 'application/json,text/javascript,*/*;q=0.01', 
		'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/65.0.3325.162Safari/537.36', 
		'Connection': 'keep-alive', 
		'Cookie':'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644; LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644; _ga=GA1.2.1514235968.1511234812; LG_LOGIN_USER_ID=87df3eb128a51a99595ac0e041c1ec2ae82012416f63916c; JSESSIONID=ABAAABAAAGFABEFAFF540316A9C596C7C95AEC19F8FC61A; _gid=GA1.2.1275640327.1528596573; LGSID=20180610100945-5873e300-6c53-11e8-9952-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527327829,1527601928,1528356179,1528596582; TG-TRACK-CODE=index_search; X_HTTP_TOKEN=9b3b4ca5be85f2540679671acec8948f; index_location_city=%E6%B7%B1%E5%9C%B3; SEARCH_ID=c51fde656e4c40c5b9afb164ccc525a8; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528596864; LGRID=20180610101453-0faf08ec-6c54-11e8-9952-525400f775ce',
		# 'Cookie': 'user_trace_token=20171121112654-d2256ffd-ce6b-11e7-9971-5254005c3644;LGUID=20171121112654-d22572b4-ce6b-11e7-9971-5254005c3644;_ga=GA1.2.1514235968.1511234812;LG_LOGIN_USER_ID=87df3eb128a51a99595ac0e041c1ec2ae82012416f63916c;JSESSIONID=ABAAABAAAGFABEFAFF540316A9C596C7C95AEC19F8FC61A;_gid=GA1.2.1275640327.1528596573;LGSID=20180610100945-5873e300-6c53-11e8-9952-525400f775ce;PRE_UTM=;PRE_HOST=;PRE_SITE=;PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F;Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1527327829,1527601928,1528356179,1528596582;_gat=1;TG-TRACK-CODE=index_search;X_HTTP_TOKEN=9b3b4ca5be85f2540679671acec8948f;index_location_city=%E6%B7%B1%E5%9C%B3;SEARCH_ID=c51fde656e4c40c5b9afb164ccc525a8;Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1528596864;LGRID=20180610101453-0faf08ec-6c54-11e8-9952-525400f775ce', 
		'Pragma': 'no-cache', 
		'Cache-Control': 'no-cache', 
		'Referer': 'https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=', 
		'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
		page = 1
		break_out=False
		while 1:
			print 'page {}'.format(page)
			data = {
			'first': 'false',
			'pn': '1',
			'kd': name
			}
			data['pn']=str(page)
			r = requests.post(url, headers=headers,data = data)
			try:
				js = r.json()
			except Exception,e:
				print e
				break
			# print js.get('content')

			if js.get('content').get('positionResult').get('totalCount')/15 < (page+3):
			# if js.get('content').get('resultSize')==0:
				break
			# if 
			if break_out:
				break

			for i in js.get('content').get('positionResult').get('result'):
				# print i.get('companyFullName'),i.get('companyShortName')
				fullname = i.get('companyFullName')
				companyId = i.get('companyId')
				# if len(companyId)==0:
				print type(companyId)
				if companyId is None:
					break_out = True
				# print fullname,companyId
				try:
					pool.set(companyId,fullname)
				except Exception,e:
					print e

			if js.get('content').get('positionResult').get('result') is None:
				break
			page+=1

# search()
# find_positionName()