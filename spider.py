#-*- coding:utf-8 -*-
"""
基于requests和urlopen可圈可点网和育星教育网
简单的爬虫用于下载资源文件
"""
import json
import random
import time,datetime
import os,sys,io
import requests
from bs4 import BeautifulSoup
import urllib2
from urllib import unquote
import urllib
import re
import urllib2
import torndb
import traceback
from multiprocessing import Pool




#from vps import connect,disconnect


reload(sys)
sys.setdefaultencoding('utf-8')

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


#######################################################################################
#初中课件
###############################################################################

db = torndb.Connection("127.0.0.1:3306", "test", user="root", password="root")


def get_step_list(ids=[],step=100):
    ids_dis_list = [[ids[i],ids[i+step]] if i<len(ids)-step \
                    else [ids[i],ids[-1]] for i in \
                        filter(lambda x:x%step==0,range(0,len(ids)))]
    return ids_dis_list


def download_zip(url,path,count=0,title="",zyid=0):
    count += 1
    local_filename = url.split('/')[-1]
    local_filename = url.split('/')[-1].split("&")[-1]+".zip"

    local_filename = os.path.join(path,local_filename)

    print(u"开始下载:{}".format(url))
    try:
        cookie = "PHPSESSID=5c51711f49cf58c84f425d65d2a1aa12; UM_distinctid=161dad13233e6-06d5ab0b437289-454c092b-100200-161dad132343be; CNZZDATA2655769=cnzz_eid%3D1736020954-1519806683-http%253A%252F%252Fftp.yinruiwen.com%252F%26ntime%3D1519806683; CNZZDATA5869936=cnzz_eid%3D950201996-1519810507-http%253A%252F%252Fftp.yinruiwen.com%252F%26ntime%3D1519810507; CNZZDATA1761520=cnzz_eid%3D1156571704-1519794296-http%253A%252F%252Fftp.yinruiwen.com%252F%26ntime%3D1519817503"
        headers = {
                        "Referer":"http://kj.5ykj.com/yi/{}.htm".format(zyid),
                        #"Referer":"http://kj.5ykj.com/yi/92.htm",
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
                        #"Cookie":cookie,
                        #"Origin":"http://www.yinruiwen.com",
                        #"Host":"ftp.yinruiwen.com"
                        "Host":"kj.5ykj.com"
                        }
        session = requests.Session()
        r = requests.get(url,timeout=30)
        print r.headers
        content_type = r.headers.get("Content-Type")
        Content_Disposition = r.headers.get("Content-Disposition",None)

        ext = ".zip"
        #print content_type,1111111
        #print Content_Disposition,2222222222222
        if "octet-stream" in content_type and Content_Disposition :
            ext = ".{}".format(Content_Disposition.split("=")[-1].split(".")[-1])
            
        #
        local_filename = url.split('/')[-1].split("&")[-1]+ext
        local_filename = os.path.split(url.split("?")[0])[-1]
        local_filename = os.path.join(path,local_filename)
        local_filename = os.path.splitext(local_filename)[0]+title+os.path.splitext(local_filename)[-1]
        print local_filename,22222222222
        if r.status_code==200 and "zip" in content_type or "octet-stream" in content_type or "office" in content_type:
            try:
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024): 
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                            #f.flush() commented by recommendation from J.F.Sebastian
                print(u"下载完成!")
                return local_filename
                return True
            except Exception as e:
                print(u"下载失败!!!")
                import traceback
                traceback.print_exc()
                download_zip(url,path)
        else:
            if count>=3:
                print(u"尝试10次下载失败!!!跳过!!!")
                return None

            download_zip(url,path,count)
    except Exception as e:
        import traceback
        traceback.print_exc()
        download_zip(url,path)



def update_download_urls(zyid,title,url,download_url):
    """更新下载地址
    """
    qsql = "select *from yinruiwen where zyid={}".format(zyid)
    if db.query(qsql):
        print u"已写入 跳过:"
    else:
        sql = "insert into yinruiwen(title,url,zyid,download_url) values('{}','{}',{},'{}')".format(title,url,zyid,download_url)
        print sql,33333333333
        db.execute(sql)
        db.close()

def parse_list_html(html=""):
    """解析列表数据返回资源ID
    """
    #soup = BeautifulSoup(html,"html5lib",from_encoding="gb2312")
    soup = BeautifulSoup(html,"html5lib",from_encoding="utf-8")
    #
    #tbls = soup.find_all("table",bgcolor="FFCB7D")
    #for _tbl in tbls:
    #    _atag = _tbl.find_all("a")
    #    _astr = str(_atag[0])

    #    title = _atag[0].text
    #    url = re.search(r'href="(.*?)"',_astr).groups()[0]
    #    zyid = os.path.split(url)[-1].split(".")[0]
    #    download_url = "http://ftp.yinruiwen.com/index.php?html=1&theid={}&download=1".format(zyid)
    #    #写入数据库
    #    update_download_urls(zyid,title,url,download_url)

    ##莲山课件
    #box1 = soup.find_all("div",id="box1")
    #print box1
    #lis = box1[0].find_all("li")
    #for _tbl in lis:
    #    _atag = _tbl.find_all("a")
    #    _astr = str(_atag[0])

    #    title = _atag[0].text
    #    url = re.search(r'href="(.*?)"',_astr).groups()[0]
    #    zyid = os.path.split(url)[-1].split(".")[0]
    #    #download_url = "http://ftp.yinruiwen.com/index.php?html=1&theid={}&download=1".format(zyid)
    #    download_url = "http://kj.5ykj.com/downLoad.asp?m=1002&id={}&downid=1".format(zyid)
    #    #写入数据库
    #    update_download_urls(zyid,title,url,download_url)

    #可圈可点网
    divs = soup.find_all("div",id="list_containers")
    #print divs,99999999999999999999
    lis = divs[0].find_all("li")
    #print lis
    for _tbl in lis:
        _atag = _tbl.find_all("a")
        _astr = str(_atag[0])

        title = _atag[0].text
        url = re.search(r'href="(.*?)"',_astr).groups()[0]
        zyid = url.split("/")[2]
        #可圈可点
        #进入下一级页面找下载链接
        url = "http://cooco.net.cn" + url
        download_html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(download_html,"html5lib",from_encoding="utf-8")
        _atag = soup.find_all("a",class_="d1")
        _astr = str(_atag[0])
        download_url = re.search(r'href="(.*?)"',_astr).groups()[0]
        #print download_url,8888888888888888888

        #download_url = "http://kj.5ykj.com/downLoad.asp?m=1002&id={}&downid=1".format(zyid)
        #写入数据库
        update_download_urls(zyid,title,url,download_url)

def get_download_url():
    """
    """
    for p in range(1,1440):
        #_list_url = "http://kj.5ykj.com/list/list_16_{}.htm".format(p)
        #可圈可点
        _list_url = "http://cooco.net.cn/23/{}.html".format(p)
        print _list_url
        html = urllib2.urlopen(_list_url).read()
        parse_list_html(html)
        #break

def process_download_task(params_tpl=()):
    """多进程下载文件
    """
    download_url = params_tpl[0]
    zyid = params_tpl[1]
    title = params_tpl[2]

    #
    #下载
    local_filename = download_zip(download_url,"/root/yinruiwen/download",0,title,zyid)
    print local_filename
    local_filename = local_filename.replace("\\","/") if local_filename else ""
    if local_filename:
        db = torndb.Connection("127.0.0.1:3306", "test", user="root", password="root")
        usql = "update yinruiwen set path='{}' where zyid={}".format(local_filename,zyid)
        print usql,666666666666
        db.execute(usql)
        db.close()


def main():
    """
    """
    #get_download_url()

    #return None

    #ids = range(1,10000)
    #ids = range(16998,20000)
    ids = range(41597,60000)
    ids_dis_list = get_step_list(ids,100)
    for _ran in ids_dis_list:
        start = _ran[0]
        end = _ran[1]
        
        tmp = []
        sql = "select *from yinruiwen where id>={} and id<{}".\
                format(start,end)
        result = db.query(sql)
        for _item in result:
            _id = _item.get("id")
            zyid = _item.get("zyid")

            with open("zyid.log","w+") as f:
                f.write(str(_id))
            f.close()

            title = _item.get("title")
            download_url = _item.get("download_url")
            
            qsql = "select *from yinruiwen where zyid={} and path is not NULL".format(zyid)
            if db.query(qsql):
                print u"已下载跳过:",zyid
                continue
            db.close()
            tmp.append((download_url,zyid,title))

            ##下载
            #local_filename = download_zip(download_url,"/root/yinruiwen/download",0,title,zyid)
            #print local_filename
            #local_filename = local_filename.replace("\\","/") if local_filename else ""
            #if local_filename:
            #    usql = "update yinruiwen set path='{}' where zyid={}".format(local_filename,zyid)
            #    print usql,666666666666
            #    db.execute(usql)
            #    db.close()
        # 
        pool=Pool(5)
        pool.map(process_download_task,tmp)

if __name__ == "__main__":
    main()
