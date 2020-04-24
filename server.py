import os.path
import re
import base64

from graphviz import Digraph

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
		treeStruct=""
		self.nodeName={}
		self.tree={}

	def __del__(self):
		self.root=1
		self.tree.clear()
		self.nodeName.clear()
		self.treeStruct=""

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


def plot_model(tree, name):
	g = Digraph("G", filename=name, format='png', strict=False)
	first_label = list(tree.keys())[0]
	g.node("0", first_label)
	_sub_plot(g, tree, "0")
	g.view()


def _sub_plot(g, tree, inc):
    root=1

    first_label = list(tree.keys())[0]
    ts = tree[first_label]
    for i in ts.keys():
        if isinstance(tree[first_label][i], dict):
            root = str(int(root) + 1)
            g.node(root, list(tree[first_label][i].keys())[0])
            g.edge(inc, root, str(i))
            _sub_plot(g, tree[first_label][i], root)
        else:
            root = str(int(root) + 1)
            g.node(root, tree[first_label][i])
            g.edge(inc, root, str(i))


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
		f.close()

class buildTreeHandler(tornado.web.RequestHandler):
	def get(self):
		f=open(fileShowed,'r')
		line=f.readline()
		flag=0

		tree=Tree()
		vec=[]		

		while line:
			if(line.strip() == "</RELATION>"):
				flag=0
				break
			
			if(flag==1):
				#relation标签内的一行，维护树结构
				kv_List=line.split()

				mp={}

				for item in kv_List:
					if(item=="<R" or item=="/>"):
						continue
					#print(item)
					key=re.findall(r"(.+?)=",item)[0]
					if(key=="ChildList"):
						continue
					val=re.findall("\""+"(.+?)"+"\"" ,item)[0]
					mp[key]=val
				
				vec.append(mp)
			
			if(line.strip() == "<RELATION>"):
				flag=1

			line = f.readline()

		#做个从值域到节点编号的映射，后面从父节点连接子节点的时候需要子节点编号
		range2NodeID={}

		mx=1
		
		#print(vec) 

		for mp in vec:
			lb=mp["ParagraphPosition"][0]
			rb=mp["ParagraphPosition"][-1]
			mx=max(mx,int(rb))
			range2NodeID[tuple((lb,rb))]=mp["ID"]
		#	print(str(lb)+"___"+str(rb)+"___"+str(range2NodeID[tuple((lb,rb))]))

		for i in range(1,mx+1):
			range2NodeID[tuple((str(i),str(i)))]=str(-i)

		for mp in vec:
			ss=mp["ParagraphPosition"].split("|")
			sonCnt=0;
			for son in ss:
				#print(son)
				lb=son[0]
				rb=son[-1]
				sonCnt+=1
				u=int(mp["ID"])
				v=int(range2NodeID[tuple((lb,rb))])
				if(mp["Center"]=="3"):
					tree.addEdge(u,v,sonCnt,mp["RelationType"])		#trick
				elif(mp["Center"]=="1" and sonCnt==1):
					tree.addEdge(u,v,1,mp["RelationType"])
				elif(mp["Center"]=="2" and sonCnt==2):
					tree.addEdge(u,v,1,mp["RelationType"])
				else:
					tree.addEdge(u,v,0,mp["RelationType"])

		tree.show(1)
		
		tmp={}	
		tmp=eval(tree.treeStruct)
		
		del tree

		#print(tmp)----------------------------------------bug
		plot_model(tmp,"struct.gv")

		with open("struct.gv.png","rb") as ff:
			b64=base64.b64encode(ff.read())
			s=b64.decode()
		self.write(s)
		ff.close()
		f.close()
		

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

