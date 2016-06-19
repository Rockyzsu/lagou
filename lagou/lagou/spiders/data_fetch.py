#-*- coding=utf-8 -*-
import urllib2,urllib,json
def lagou(url):
    user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header={"User-Agent":user_agent}
    post_data=urllib.urlencode({"first":"false","pn":"2","kd":"android"})
    req=urllib2.Request(headers=header,url=url,data=post_data)
    resp=urllib2.urlopen(req)
    data = resp.read()
    json_data=json.loads(data)
    #print data
    print json_data.keys()


def json_process(json_data):
    js=json.loads(json_data)
    print js.keys()
    result= js['content']['positionResult']['result']
    for i in result:
        print i['salary']

url="http://www.lagou.com/jobs/positionAjax.json?city=%e4%b8%9c%e8%8e%9e&needAddtionalResult=false"
#lagou(url)
json_file="json_data.json"
json_data=open(json_file,'r').read()
json_process(json_data)
