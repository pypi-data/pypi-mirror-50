import requests
import json 

headers={
	'content-type':'application/json;charset=utf-8'
}

def get(url):
	res = requests.get(url, headers=headers)
	return res.text

def post(url, msg):
	data = msg if isinstance(msg, str) else tojson(msg)
	res = requests.post(url, data=data, headers=headers)
	return res.text

def tojson(msg):
	return json.dumps(msg, ensure_ascii=False)

def tobean(msg):
	return json.loads(msg)