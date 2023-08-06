#!usr/bin/env python
# encoding:utf-8
from __future__ import division

"""
__Author__:沂水寒城
功能： 指定项目下载
"""


import os
import re
import time
import json
import queue
import urllib
import random
import zipfile
import requests
import threading
import urllib.request as urllib2
from optparse import OptionParser
from fake_useragent import UserAgent


USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]


#UserAgent伪装
headers = {
            'User-Agent': random.choice(USER_AGENT_LIST),
            'Connection': 'keep-alive',
            'Accept-Encoding': 'identity',
          }

#IP代理池构建
ip_list=[
         ["HTTP", "125.123.143.78", "9000"], 
         ["HTTP", "183.33.128.4", "9797"], 
         ["HTTP", "125.46.0.62", "53281"], 
         ["HTTP", "219.159.38.208", "56210"], 
         ["HTTP", "112.95.224.58", "8118"], 
         ["HTTPS", "125.123.143.16", "9000"], 
         ["HTTPS", "222.220.99.112", "8118"], 
         ["HTTP", "222.221.11.119", "3128"], 
         ["HTTP", "202.204.121.126", "80"], 
         ["HTTP", "219.159.38.204", "56210"], 
         ["HTTPS", "182.18.13.149", "53281"], 
         ["HTTPS", "58.17.125.215", "53281"], 
         ["HTTPS", "220.180.50.14", "53281"], 
         ["HTTP", "124.207.82.166", "8008"], 
         ["HTTPS", "203.86.26.9", "3128"], 
         ["HTTP", "180.168.198.141", "18118"], 
         ["HTTPS", "163.125.18.182", "8888"], 
         ["HTTP", "119.145.2.99", "44129"]
        ]

        

def single(username,projectname,path,branch_name='master'):
    '''
    单个项目处理模块
    '''
    ip_proxy=random.choice(ip_list)
    one_type,one_ip,one_port=ip_proxy[0],ip_proxy[1],ip_proxy[2]
    proxy={one_type:one_type+'://'+one_ip+':'+one_port}
    url='https://codeload.github.com/{}/{}/zip/{}'.format(username,projectname,branch_name)
    filename=path+'/'+projectname
    zipfile_name=filename+'.zip'
    data=None
    try:
        data=urllib2.urlopen(url)
        with open(zipfile_name,'wb') as f:
            f.write(data.read())
        with zipfile.ZipFile(zipfile_name, 'r') as f:
            f.extractall(path+'.')
        print('geting http://github.com/'+username+'/'+projectname)
    except (urllib.error.URLError):
        try:
            headers['Host']='github.com'
            request=requests.get('https://github.com/{}/{}'.format(username,projectname),
                                 headers=headers,proxies=proxy,timeout=5)
            response=urllib2.urlopen(request)
            pattern='/{}/{}/tree/(.*?)/'.format(username,projectname)
            b_name=re.findall(pattern, str(response.read()))[-1]
            single(username,projectname,path,b_name)
        except Exception as e:
            print('Exception: ',e)
            pass


def kwSearch(keyword,topN=50):
    '''
    基于关键词实现相关项目的搜索
    '''
    res_list=[]
    for i in range(1,topN+1):
        res=requests.get('https://api.github.com/search/repositories?q=%s&sort=updated&order=desc&page=%s' % (keyword, i))
        repo_list = res.json()['items']
        for repo in repo_list:
            repo_name=repo['html_url']
            if repo_name not in res_list:
                res_list.append(repo_name)
        time.sleep(10)
    return res_list


def urlHandle(one_url):
    '''
    项目链接处理，返回： 用户名、项目名
    https://github.com/yishuihanhan/myBooks ==> yishuihanhan、myBooks
    '''
    username,projectname=one_url.strip().split('/')[-2:]
    return username,projectname


def downloader(project_list,directory='downloadProjects/'):
    '''
    项目下载器
    '''
    threads=[]
    if not os.path.exists(directory):
        os.makedirs(directory)
    for one_list in project_list:
        username,projectname=one_list
        t=threading.Thread(target=single, args=(username,projectname,directory))
        threads.append(t)
    for t in threads:
        time.sleep(1)
        t.start()


def gitSpider(kw='spider',topN=50,saveDir='downloadProjects/'):
    '''
    github爬虫
    '''
    repo_list=kwSearch(kw,topN=topN)
    download_list=[]
    for one_url in repo_list:
        username,projectname=urlHandle(one_url)
        download_list.append([username,projectname])
    print('Downloading......')
    downloader(download_list,directory=saveDir)
    print('Finished......')


if __name__ == '__main__':
    gitSpider(kw='lstm',topN=2,saveDir='downloadProjects/')
