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


	
tr=Tree()
tr.addEdge(1,-1,1,"apple")
tr.addEdge(1,3,0,"apple")
tr.addEdge(3,-2,1,"pine")
tr.addEdge(3,-3,0,"pine")
tr.show(1)
print(tr.treeStruct)

#		1
#		/ \
#	  -1  3
#		   /\
#	     -2 -3
