import tornado.web
import tornado.ioloop
import tornado.httpserver
import os.path
import engine


class Application(tornado.web.Application):
	def __init__(self):
		self.shortener = engine.Shortener()
		
		handlers = [
			(r'/', IndexHandler),
			(r'/(.+)', HashHandler)
		]
		
		settings = {
			"template_path": "templates",
			"static_path": "static"
		}
		
		tornado.web.Application.__init__(self, handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('form.html', title='Short.er')
	
	def post(self):
		url = self.get_argument('u')
		
		if not (url.startswith('http://') or url.startswith('https://')):
			url = 'http://' + url
		
		shortened = 'http://' + self.request.host + '/' + self.application.shortener.add(url)
		self.set_status(201)
		self.set_header('Location', shortened)
		self.render('short.html', title='Short.er', url=shortened)


class HashHandler(tornado.web.RequestHandler):
	def get(self, key):
		url = self.application.shortener[key]
		if url:
			self.set_status(302)
			self.set_header('Location', url)
		else:
			self.set_status(404)
			self.write('Not found')


if __name__ == '__main__':
	from tornado.options import options, define, parse_command_line
	
	define("port", default=8000, help="listen port", type=int)
	parse_command_line()
	
	server = tornado.httpserver.HTTPServer(Application())
	server.listen(options.port, "127.0.0.1")
	
	tornado.ioloop.IOLoop.instance().start()