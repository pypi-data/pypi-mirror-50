import requests
import os,json,random

class session(object):
	def __init__(self,username,password):
		self.api_test="https://api.myip.com"
		self.countries=["al", "ar", "am", "au", "at", "az", "bd", "by", "be", "bo", "br",
			"bg", "kh", "ca", "cl", "cn", "co", "cy", "cz", "dk", "do", "ec", "eg",
			"ee", "fi", "fr", "ge", "de", "gr", "gt", "hk", "hu", "is", "in", "id",
			"ie", "il", "it", "jm", "jp", "jo", "kz", "kr", "kg", "la", "lv", "lt",
			"lu", "my", "mx", "md", "ma", "nl", "nz", "no", "pk", "pa", "pe", "ph",
			"pl", "pt", "ro", "ru", "sa", "sg", "sk", "za", "es", "lk", "se", "ch",
			"tw", "tj", "th", "tr", "tm", "ua", "ae", "gb", "us", "uz", "vn"]
		self.cc=True


		self.username=username
		self.password=password

		self.port = 22225
		self.dynamic=True
		self.host="zproxy.lum-superproxy.io"

		return None
	def generate_proxies(self,**kwargs):



		if type(self.cc)==bool:
			_country_code="-country-{}".format(random.choice(self.countries)) if self.cc else ""
		else:
			_country_code="-country-{}".format(self.cc[:2].lower())

		res={}
		for schema in ["http","https"]:
			res[schema]="{schema}://{username}{route}{country_code}:{password}@{host}:{port}".format(schema=schema,username=self.username,
			route="-route_err-pass_dyn" if self.dynamic else "-route_err-block",
			country_code=_country_code, password=self.password,port=self.port,host=self.host
			)

		return res
	def get(self,url, **kwargs):


		session=requests.session()
		session.proxies=self.generate_proxies(**kwargs)

		return session.get(url,**kwargs)
	def test(self,**kwargs):
		return self.get(self.api_test,**kwargs).json()

if __name__=="__main__":
	sess=session("{username}","{password}")
	print(sess.test())
