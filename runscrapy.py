import requests
import json
import re
import random
import time
import pymysql
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from sshtunnel import SSHTunnelForwarder
import wechat_public_login
import auto_mail
import logging
import log_config
logger = log_config.log('scrapy')
sleeptime=1200
def mysqldb():
        server = SSHTunnelForwarder(
        ssh_address_or_host=('192.168.1.245', 22),  # 指定ssh登录的跳转机的address
        ssh_username='root',  # 跳转机的用户
        ssh_password='',  # 跳转机的密码
        remote_bind_address=('127.0.0.1', 3306))
        server.start()
        connection = pymysql.connect(host='localhost',
                                     user='tgene',
                                     password='Tgylocal&17',
                                     db='tgene',
                                     port=server.local_bind_port,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return (server,connection)
def timestamp_convert(timestamp):
    date=datetime.fromtimestamp(timestamp)
    return(date)
   
def alert_pattern(list):
    alert_list=[]
    for i in list:
        a="\w*%s\w*"%i
        alert_list.append(a)
    return (('|').join(alert_list))
    
        
        
def parse_article(url,title,alert_list):
    alert=[]
    response=requests.get(url,verify=False)
    html_doc=response.text
    soup= BeautifulSoup(html_doc, 'html.parser')
    content = soup.find(id="js_content")
    plain_text=title+' '+content.get_text()
    alert=re.findall(alert_list,plain_text)
    if alert==[]: 
        alert=''
    else: alert=alert[0]
    nickname=soup.find(attrs={"class":"profile_nickname"}).text
    logger.info("%s %s"%(nickname,title))
    return (nickname,alert)

def read_cookies():
    with open('cookie.txt', 'r', encoding='utf-8') as f:
        cookie = f.read()
    cookies = json.loads(cookie)
    return cookies
    
def cookies_verify():
    url = 'https://mp.weixin.qq.com'
    header = {
        "HOST": "mp.weixin.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0"
        }
     
    cookies=read_cookies()
    response = requests.get(url=url, cookies=cookies)
    try:
        token = re.findall(r'token=(\d+)', str(response.url))[0]
        return(token,cookies,header)
    except:
        logger.info("cookie已失效")
        renew_flag=1
        for i in range(5):  #重试5次
            renew_flag = wechat_public_login.renew()
          #  logger.info(renew_flag)
            if renew_flag==0:
                cookies=read_cookies()
                response = requests.get(url=url, cookies=cookies)
                token = re.findall(r'token=(\d+)', str(response.url))[0]
                return(token,cookies,header)
                break
            else: 
                time.sleep(600)
                continue
            
        if renew_flag!=0:
            logger.info("登录错误，退出程序")
            
            return (1,1,1)
            
def main_run():        
    try:
      #  alert_words=['公布','通知']
        
        server,connection=mysqldb()
        cursor = connection.cursor()        
       # gzlist = ['MjM5NTA5NzYyMA==','MzI1MzA5MDEyNQ==']
        sql_alert="Select * from tgene.wechat_alert_words"
        cursor.execute(sql_alert)
        row_alert = cursor.fetchall()
        alert_words=[]
        for i in row_alert:
            alert_words.append(i['words']) 
        alert_list=alert_pattern(alert_words)
       # logger.info(alert_list)
            
        sql_gzlist="Select fakeid,nickname from tgene.wechat_public_id"
        cursor.execute(sql_gzlist)
        row_gzlist = cursor.fetchall()
        gzlist=[]
        nick_fake={}
        for i in row_gzlist:
            gzlist.append(i['fakeid'])
            nick_fake[i['fakeid']]=i['nickname']
       # logger.info(gzlist)
        
        for fakeid in gzlist:
            token,cookies,header=cookies_verify()
            if token==1 : return 1  #登录异常，退出
            logger.info("获取token成功,读取公众号 %s"%nick_fake[fakeid])
            appmsg_url = 'https://mp.weixin.qq.com/cgi-bin/appmsg?'
            num = 5
            begin = 0
           # fakeid= "MjM5NTA5NzYyMA=="
            query_id_data = {
                'token': token,
                'lang': 'zh_CN',
                'f': 'json',
                'ajax': '1',
                'random': random.random(),
                'action': 'list_ex',
                'begin': '{}'.format(str(begin)),
                'count': '5',
                'fakeid': fakeid,
                'type': '9'
            }

            query_fakeid_response = requests.get(appmsg_url, cookies=cookies, headers=header, params=query_id_data)
            try:
                if query_fakeid_response.json().get('base_resp')['err_msg']=='freq control':
                    logger.info("抓取过于频繁，需要退出")
                    return 1
            except:
                pass
            fakeid_list = query_fakeid_response.json().get('app_msg_list')
            #print(1)
            sql="Select aid from tgene.wechat_article where fakeid='%s'"%(fakeid)
            cursor.execute(sql)
            row1 = cursor.fetchall()
            aid_list=[]
            if row1==[]: row1=[{'aid':1}]           
            for i in row1:
                aid_list.append(i['aid'])  
            new=0
            old=0
            for item in fakeid_list:               
                if item.get('aid') not in aid_list:
                    nickname,alert=parse_article(item.get('link'),item.get('title'),alert_list)
                    sql="INSERT INTO tgene.wechat_article VALUES ('%s','%s','%s','%s','%s','%s','%s');"%(item.get('aid'),timestamp_convert(item.get('create_time')),item.get('title'),item.get('link'),fakeid,nickname,alert)
                   
                    cursor.execute(sql)
                    connection.commit()
                    time.sleep(5)
                    new+=1
                else:
                    old+=1
                    #logger.info("已经存在的消息")
            logger.info("新增记录%s条 已存在记录%s条"%(new,old))
            sql_log="UPDATE tgene.wechat_public_id SET lastest_scan='%s', scan_counts=scan_counts+1 where fakeid='%s'"%(datetime.now(),fakeid)
            cursor.execute(sql_log)
            connection.commit()
            logger.info("公众号记录更新成功，等待%s秒后开始下一个抓取"%sleeptime)
            time.sleep(sleeptime)   #公众号直接的等待时间
        connection.close()
        server.stop()
        return 0
    except Exception as e:
        logger.info('%s'%e)
        connection.close()
        server.stop()
        return 1

while 1:
    logger.info("开始爬取公众号")
    if (main_run()!=0):
        logger.info("程序异常退出")
        
        break
    time.sleep(sleeptime)
auto_mail.AlertMsg("公众号程序异常","尝试登录次数过多，需要重启程序")
sys.exit()
