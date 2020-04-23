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

class Tree:		#{[(,,),()],[]}
	root = 1
	tree={}
	nodeName={}		##########RelationType
	treeStruct=""

	def __init__(self):		
		self.root=1
		
	def addEdge(self,u,v,val,uname):
		if u in self.tree:
			self.tree[u].append(tuple((v,val)))
			self.nodeName[u]=str(uname)
		else:
			self.tree.setdefault(u,[])
			self.tree[u].append(tuple((v,val)))
			self.nodeName[u]=str(uname)

	def show(self,now):
		if(now < 0): #####叶子
			self.treeStruct+="\""+str(-now)+"\""
			return
		self.treeStruct+="{"+"\""+str(self.nodeName[now])+"\""	#{

		self.treeStruct+=":{"		
		for item in self.tree[now]:
			newName=item[1]
			self.treeStruct+=str(newName)+":"
			self.show(int(item[0]))
			if(item!=self.tree[now][-1]):
				self.treeStruct+=","
		self.treeStruct+="}"
		self.treeStruct+="}"		#}

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

		tree=Tree()

		while line:
			if(line.strip() == "<RELATION>"):
				flag=1
				continue

			if(line.strip() == "</RELATION>"):
				flag=0
				break
			
			if(flag==1):
				#relation标签内的一行，维护树结构
				kv_List=line.split()

				fa=-1
				sons=[]

				for item in kv_List:
					if(item=="<R" or item=="/>"):
						continue
					key=re.findall(r"(.+?)=",item)[0]
					val=re.findall("\""+"(.+?)"+"\"" ,item)[0]

					if(key=="ID"):
						lineID=int(val)
					if(key=="ParagraphPosition"):
						ss=val.split("|")
						for sonsCover in ss:
							if(sonsCover[0]==sonsCover[-1]):
								sons.
			
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

