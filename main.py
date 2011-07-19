import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import os.path
import engine

import logging


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('welcome')
	
	def post(self):
		url = self.get_argument('u')
		shortened = self.application.shortener.add(url)
		self.write('http://%s/%s' % (self.request.host, shortened))


class HashHandler(tornado.web.RequestHandler):
	def get(self, key):
		url = self.application.shortener[key]
		if url:
			self.set_status(302)
			self.set_header('Location', url)
		else:
			self.set_status(404)
			self.write('Not found')


class Application(tornado.web.Application):
	def __init__(self):
		self.shortener = engine.Shortener()
		
		handlers = [
			(r'/', IndexHandler),
			(r'/([A-Za-z0-9-_]{8})', HashHandler)
		]
		
		settings = {
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
			"template_path": os.path.join(os.path.dirname(__file__), "templates"),
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
	tornado.options.define("port", default=8000, help="listen port", type=int)
	tornado.options.define("address", default=None, help="listen address", type=str)
	tornado.options.parse_command_line()
	
	server = tornado.httpserver.HTTPServer(Application())
	
	if tornado.options.options.address:
		server.listen(tornado.options.options.port, tornado.options.options.address)
	else:
		server.listen(tornado.options.options.port)
	
	tornado.ioloop.IOLoop.instance().start()
