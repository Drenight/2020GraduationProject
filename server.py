import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html')

class preFileCountHandler(tornado.web.RequestHandler):
	def get(self):
		prePath=os.getcwd()+"/pre"
		preFileCnt=os.listdir(prePath)
		self.write(str(preFileCnt))

class tagFileCountHandler(tornado.web.RequestHandler):
	def get(self):
		dataPath=os.getcwd()+"/data"
		dataFileCnt=os.listdir(dataPath)
		self.write(str(dataFileCnt))

class showFileHandler(tornado.web.RequestHandler):
	def get(self):
		dataPath=os.getcwd()+"/data/"
		dataPath+=str(self.get_argument("message"))
		f=open(dataPath,'r')
		self.write(str(f.read()))


if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[
		(r'/', IndexHandler), 
		(r'/preFileCount',preFileCountHandler),
		(r'/tagFileCount',tagFileCountHandler),
		(r'/showFile',showFileHandler),
		]
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
