from hashlib import sha1
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64decode

class Shortener(object):
	def __init__(self):
		self.urlMap = {}
	
	def add(self, url):
		d = sha1(url).digest()[0:5]
		u = 0
		
		while d + chr(u) in self.urlMap and self.urlMap[d + chr(u)] != url:
			u += 1
		
		self.urlMap[d + chr(u)] = url
		return urlsafe_b64encode(d + chr(u))
	
	def __getitem__(self, key):
		return self.urlMap.get(urlsafe_b64decode(key), None)