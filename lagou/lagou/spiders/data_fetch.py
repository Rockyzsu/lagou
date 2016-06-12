#-*- coding=utf-8 -*-
import urllib2,urllib
def lagou(url):
    user_agent="Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header={"User-Agent":user_agent}
    post_data=urllib.urlencode({"first":"true","pn":"1","kd":"android"})
    req=urllib2.Request(headers=header,url=url,data=post_data)
    resp=urllib2.urlopen(req)
    print resp.read()





url="http://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
lagou(url)
