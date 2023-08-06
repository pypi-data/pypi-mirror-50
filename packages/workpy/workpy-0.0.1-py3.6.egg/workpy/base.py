import os
import requests

def llist(s):
	return [i.split() for i in s.split('\n') if len(i) > 0]

def hump(s):
	a = [i for i in uline(s).split('_') if len(i) > 0]
	return a[0].lower()+''.join(i.capitalize() for i in a[1:])

def uline(s):
	b = ''
	a = str(s)
	for i, v in enumerate(a):
		b += '_'+v if v.isupper() and a[i-1].islower() else v
	return '_'.join([i.lower() for i in b.split('_') if len(i) > 0])

def post(url, msg):
	headers={'context-type':'application/json;charset=utf-8'}
	res = requests.post(url, data=msg, headers=headers)
	return res.text

def get(url):
	headers={'context-type':'application/json;charset=utf-8'}
	res = requests.get(url, data=msg, headers=headers)

if __name__ == '__main__':
	pass
	print(get('http://localhost/help/index.html'))