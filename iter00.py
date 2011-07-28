import tornado.web
import tornado.ioloop
import tornado.httpserver
import os.path


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r'/', IndexHandler),
		]
		
		tornado.web.Application.__init__(self, handlers)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('Hello\n')

if __name__ == '__main__':
	from tornado.options import options, define, parse_command_line
	
	define("port", default=8000, help="listen port", type=int)
	parse_command_line()
	
	server = tornado.httpserver.HTTPServer(Application())
	server.listen(options.port, "127.0.0.1")
	
	tornado.ioloop.IOLoop.instance().start()
