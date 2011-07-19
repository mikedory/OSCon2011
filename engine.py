from hashlib import sha1
from base64 import urlsafe_b64encode as base64encode
from base64 import urlsafe_b64decode as base64decode

class Shortener(object):
	def __init__(self):
		self.urlMap = {}
	
	def add(self, url):
		digest = sha1(url).digest()[0:5]
		unique = 0
		
		while digest + chr(unique) in self.urlMap and self.urlMap[digest + chr(unique)] != url:
			unique += 1
		
		self.urlMap[digest + chr(unique)] = url
		return base64encode(digest + chr(unique))
	
	def __getitem__(self, key):
		return self.urlMap.get(base64decode(key), None)