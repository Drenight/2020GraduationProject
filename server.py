import os.path
import re

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

#正在展示的文件名全局变量
fileShowed="-1"


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
		dataPath=str(os.getcwd())
		dataPath+=str(self.get_argument("message"))

		global fileShowed
		fileShowed=dataPath

		f=open(dataPath,'r')
		self.write(str(f.read()))

class buildTreeHandler(tornado.web.RequestHandler):
	def get(self):
		f=open(fileShowed,'r')
		line=f.readline()
		flag=0

		treeRoot=-1
		treeGraph={}

		while line:
			if(line.strip() == "</RELATION>"):
				break
			
			if(flag==1):
				#relation标签内的一行，维护树结构
				kv_List=line.split()
				for item in kv_List:
					if(item=="<R" or item=="/>"):
						continue
					key=re.findall(r"(.+?)=",item)[0]
					val=re.findall("\""+"(.+?)"+"\"" ,item)[0]

					#########todo
			
			if(line.strip() == "<RELATION>"):
				flag=1
			
			line = f.readline()

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = tornado.web.Application(
		handlers=[
		(r'/', IndexHandler), 
		(r'/preFileCount',preFileCountHandler),
		(r'/tagFileCount',tagFileCountHandler),
		(r'/showFile',showFileHandler),
		(r'/buildTree',buildTreeHandler),
		]
	)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()

