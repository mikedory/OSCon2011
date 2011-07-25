import tornado.web
import tornado.ioloop
import tornado.httpserver
import os.path
import engine


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('Hello')
	
	def post(self):
		url = self.get_argument('u')
		shortened = url[0:8]
		self.set_status(201)
		self.set_header('Location', 'http://%s/%s' % (self.request.host, shortened))
		self.write('http://%s/%s\n' % (self.request.host, shortened))


class HashHandler(tornado.web.RequestHandler):
	def get(self, key):
		self.write('Your requested hash: ' + key)
	
	# def get(self, key):
	# 	url = self.application.shortener[key]
	# 	if url:
	# 		self.set_status(302)
	# 		self.set_header('Location', url)
	# 	else:
	# 		self.set_status(404)
	# 		self.write('Not found')


class Application(tornado.web.Application):
	def __init__(self):
		self.shortener = engine.Shortener()
		
		handlers = [
			(r'/', IndexHandler),
			(r'/([A-Za-z0-9-_]+)', HashHandler)
		]
		
		settings = {
			"static_path": os.path.join(os.path.dirname(__file__), "static"),
			"template_path": os.path.join(os.path.dirname(__file__), "templates"),
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
	from tornado.options import options, define, parse_command_line
	
	define("port", default=8000, help="listen port", type=int)
	parse_command_line()
	
	server = tornado.httpserver.HTTPServer(Application())
	server.listen(options.port, "127.0.0.1")
	
	tornado.ioloop.IOLoop.instance().start()
