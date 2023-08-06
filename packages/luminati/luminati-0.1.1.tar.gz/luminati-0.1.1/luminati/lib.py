import requests
import os,json,random

timeout=None
headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
api_test="https://api.myip.com"
cc=True


dynamic=True
#username="lum-customer-hl_7c6aa799-zone-zone1"
#password = '7nli0zglq1l2'
username=""
password=""
port = 22225
dynamic=True
host="zproxy.lum-superproxy.io"

countries=json.load(open("countries.json","r+"))
countries=list(filter(lambda item: item[0]==item[1]['cc'].lower() ,countries.items()))
countries=list(map(lambda item:item[0],countries))

def generate_proxies(**kwargs):
	_username=kwargs['username'] if "username" in kwargs else username
	_password=kwargs['password'] if "password" in kwargs else password
	_port=kwargs['port'] if "port" in kwargs else port
	_dynamic=kwargs['dynamic'] if "dynamic" in kwargs else dynamic
	_cc=kwargs['cc'] if "cc" in kwargs else cc
	if type(_cc)==bool:
		_country_code="-country-{}".format(random.choice(countries)) if _cc else ""
	else:
		_country_code="-country-{}".format(_cc)

	res={}
	for schema in ["http","https"]:
		res[schema]="{schema}://{username}{route}{country_code}:{password}@{host}:{port}".format(schema=schema,username=_username,
		route="-route_err-pass_dyn" if dynamic else "-route_err-block",
		country_code=_country_code, password=_password,port=_port,host=host
		)
	return res
def get(url, **kwargs):


	session=requests.session()
	session.proxies=generate_proxies(**kwargs)
	return session.get(url,headers=headers,timeout=timeout)
def test(**kwargs):
	return get(api_test,**kwargs).json()
if __name__=="__main__":

	print(test())
