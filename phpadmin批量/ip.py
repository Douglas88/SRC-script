#!/bin/usr/env python3

import requests, json, re, copy, time

url = 'https://api.zoomeye.org/host/search?query='

def login(username, password):
	data = {
		'username': '499744187@qq.com',
		'password': 'zhangfei66217985',
	}
	data = json.dumps(data)
	resp = requests.post(url='https://api.zoomeye.org/user/login', data=data)
	res = resp.text
	res_data = json.loads(res)
	return json.loads(resp.text)['access_token']

def search(token, query):
	headers = {
		'Authorization': 'JWT {}'.format(token),
	}
	resp = requests.get(url='https://api.zoomeye.org/host/search?query={}'.format(query), headers=headers)
	return json.loads(resp.text)

def get_valid(resultSet, keyWord):
	index = 0
	del_list = []
	for i in resultSet['matches']:
		if(keyWord not in i['portinfo']['banner']):
			#不符合条件
			del_list.append(index)
		index+=1
	
	#删除不符合的项
	for i in reversed(del_list):
		resultSet['matches'].pop(i)
	return resultSet

def get_ip(resultSet):
	f = open("ip.txt", "a+")
	for i in resultSet['matches']:
		print(i['ip'])
		ip = i["ip"]
		f.write(ip + "\n")

	f.close()
		
def get_ipAndPort(resultSet):
	for i in resultSet['matches']:
		print(i['ip']+":"+str(i['portinfo']['port']))
			
def get_ipAndWebBanner(resultSet):
	for i in resultSet['matches']:
		ip = i['ip']
		banner = get_webBanner(ip)
		if(banner == 'false'):
			print(ip)
		else:
			try:
				print(ip+"     "+banner[0])
			except:
				print(ip)
			
def banner(resultSet):
	index = 0
	for i in resultSet['matches']:
		print('{}'.format(index))
		print(i['portinfo']['banner'])
		index += 1	
			
def get_webBanner(ip):
	try:
		resp = requests.get('http://'+ip, timeout=3)
		if(resp.status_code == 200):
			pattern = re.compile('<title>(.*?)</title>', re.S)
			res = re.findall(pattern, resp.text)
			return res
		else:
			return 'false'
	except requests.exceptions.ConnectTimeout:
		return 'false'
	except requests.exceptions.Timeout:
		return 'false'
	except requests.exceptions.ConnectionError:
		return 'false'
			
if __name__ == '__main__':

	username = '499744187@qq.com'
	password = 'zhangfei66217985'
	token = login(username, password)
	#获取1-10页zoomeye记录
	for x in range(0, 5):
		query = 'phpStudy%20Country%3ACN&page={}'.format(x)
		
		resultSet = search(token, query)
		rawResult = copy.deepcopy(resultSet)

		#print('raw ip-->>')
		#get_ip(resultSet)
		
		resultSet = get_valid(resultSet, '')

		
		#print('get valid-->>')
		get_ip(resultSet)
		print("No.{}---->>>>".format(x))
		get_ipAndWebBanner(resultSet)

		time.sleep(8)
	
