#coding: utf-8
#不去重复网页
#增加搜索完自动调用sqlmap功能
#改为多线程
import urllib2
import string
import urllib
import re
import random
from urlparse import urlparse
import sys,os
from Queue import  Queue
import threading

user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0', \
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', \
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \
        (KHTML, like Gecko) Element Browser 5.0', \
        'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)', \
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', \
        'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14', \
        'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \
        Version/6.0 Mobile/10A5355d Safari/8536.25', \
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/28.0.1468.0 Safari/537.36', \
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']

def baidu_search(keyword,pn):
    p= {'wd': keyword}
    searchurl=("http://www.baidu.com/s?"+urllib.urlencode(p)+"&pn={0}&cl=3&rn=100").format(pn)
    print searchurl
    res=urllib2.urlopen(searchurl, timeout = 15)
    html=res.read()
    if len(html) < 200:
        print html
        print "----------------------------------------------"
    if "window.location.href" in html:
        searchurl2 = html.split("\'")
        res=urllib2.urlopen(searchurl2[1], timeout = 15)
        print searchurl2[1]
        html = res.read()
        if len(html) < 200:
            print html
            print "=========================="
    return html


def getbaiduurl(html,Q):
    l_htm = html.split('\n')
    for tx in l_htm:
        if 'href =' in tx:
            url=tx.split('\"')
            #arr.append(url[1])
            Q.put(url[1])

def getRealUrl(urlq, urllist):
    while urlq.empty() is not True:
        item = urlq.get()
        try:
            print "Origin link is:"+item
            domain=urllib2.Request(item)
            r=random.randint(0,11)
            domain.add_header('User-agent', user_agents[r])
            domain.add_header('connection','keep-alive')
            response=urllib2.urlopen(domain, timeout = 15)
            uri=response.geturl()
            print "The true link is:"+uri
            if 'baidu' not in uri:
                urllist.append(uri)
        except:
            print 'Exception occur!!!'


def url_exist(real_url, netloc):
    for url_temp in real_url:
        if netloc in url_temp:
            return 1


def write_url(real_url):
    result = open("url.txt","w")
    for i in real_url:
        result.write(i + '\n')
    result.close()


def geturl(keyword,Q):
    for page in range(10):
        pn=page*100+1
        html = baidu_search(keyword,pn)# html type is string
        #print type(html)
        getbaiduurl(html,Q)
        #print arr
def writeQ(url_queue,item):
    url_queue.put(item)
def readQ(url_queue,item):
    return url_queue.get()

class MyThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        #self.name = name
    def run(self):
        apply(self.func, self.args)

def main():
    url_queue = Queue(200)
    key=raw_input("Please input keyword:")
    geturl(key, url_queue)
    print 'queue size:',url_queue.qsize()
    result = open("url3.txt","w")
    urllist = []
    #getRealUrl(url_queue,urllist)
    threads = []
    for i in range(10):
        t = MyThread(getRealUrl,(url_queue,urllist))
        threads.append(t)
    for i in range(10):
        threads[i].start()
    for i in range(10):
        threads[i].join()
    for u in urllist:
        result.write(u + '\n')
    result.close()
    #增加自动调用sqlmap扫描功能
    #php脚本
    '''
    print 'key is : ',key
    if 'php' in key:
        os.system("python D:\share\web\sqlmap\sqlmap.py --proxy=http://10.41.70.8:80 --random-agent --time-sec=10  --tamper tamper\space2morehash.py --batch -m url.txt -b")
    #asp脚本
    else:
        os.system("python D:\share\web\sqlmap\sqlmap.py --proxy=http://10.41.70.8:80 --random-agent --time-sec=10  --tamper tamper\charunicodeencode.py --batch -m url.txt -b")
   '''
if __name__=='__main__':
    main()
