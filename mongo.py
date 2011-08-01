from hashlib import sha1
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64decode

import pymongo

class Shortener(object):
	def __init__(self):
		c = pymongo.Connection('mongodb://oscon:12345@staff.mongohq.com:10083/oscon')
		self.database = c.oscon
		self.urlMap = {}
	
	def add(self, url):
		d = sha1(url).digest()[0:5]
		u = 0
		
		cursor = self.database.urls.find({"_id": d})
		
		for i in cursor:
			
		while d + chr(u) in self.urlMap and self.urlMap[d + chr(u)] != url:
			u += 1
		
		self.urlMap[d + chr(u)] = url
		return urlsafe_b64encode(d + chr(u))
	
	def __getitem__(self, key):
		try:
			digest = urlsafe_b64decode(str(key))
		except TypeError as e:
			return None
		
		cursor = self.database.urls.find({"_id": d[0:5]})
		
		if not cursor.count():
			return None
		
		item = cursor.next()
		
		item
		
		return item['url'][d[5]]