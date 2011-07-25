import tornado.web
import tornado.ioloop
import tornado.httpserver
import os.path


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', IndexHandler),
			(r'/(.+)', HashHandler)
		]
		
		tornado.web.Application.__init__(self, handlers)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('Hello\n')
	
	def post(self):
		url = self.get_argument('u')
		shortened = 'http://' + self.request.host + '/' + url[:8]
		self.set_status(201)
		self.set_header('Location', shortened)
		self.write(shortened + '\n')


class HashHandler(tornado.web.RequestHandler):
	def get(self, key):
		self.write('You requested a page with this hash: %s\n' % key)


if __name__ == '__main__':
	from tornado.options import options, define, parse_command_line
	
	define("port", default=8000, help="listen port", type=int)
	parse_command_line()
	
	server = tornado.httpserver.HTTPServer(Application())
	server.listen(options.port, "127.0.0.1")
	
	tornado.ioloop.IOLoop.instance().start()