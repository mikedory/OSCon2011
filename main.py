#!/usr/bin/env python

# python basics
import os.path

# tornado things
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.database
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

# define Tornado defaults
define("port", default=8000, help="run on the given port", type=int)

# settings
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			)
		tornado.web.Application.__init__(self, handlers, **settings)


# handle the main page
class MainHandler(tornado.web.RequestHandler):
	def get(self):

		# show it up
		self.render(
			"index.html",
			title="title",
			header="header"
		)


# start it up
def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
		main()
