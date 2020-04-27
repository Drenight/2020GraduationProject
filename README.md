failed to execute ['dot', '-Tpng', '-O', 'struct.gv'], make sure the Graphviz executables are on your systems' PATH
UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8

HTTP304
200 GET /buildTree (127.0.0.1) 55.21ms
304 GET /buildTree (112.20.40.109) 1.69ms

### 结构
raw:生语料
pre:预处理后文件
data:已标注文件

#### 20200416 
- 疑问，MCDTB的raw文件夹里存的应该都是被预处理过的文件吧，生语料后缀好像是带有raw的
- 前后端采用ajax成功交互
- 第一个按钮【显示服务器上的语料数】功能的实现
- 落盘操作应该不用单独分出来了，服务器后端python做完预处理就直接保存

#### 20200420
- 前端视图开发中……
- 后端write xml文件内容后，刷新p节点的innerHTML无法显示xml标签，被浏览器理解为h5标签，把p改成xml之后fix

#### 20200421
- 开发树形结构展示功能
- MCDTB语料库中的文章RelationNumber标签都是单个关系，先照此开发吧
- 思路是遍历parentID，建出关系节点的邻接表；然后遍历ParagraphPosition连接叶子节点。
- 考虑python处理字符串更熟，打算后端建树，找找画图的包画个图出来传base64码给前端解

#### 20200422
- 开发树形结构展示功能
- 逐行处理RELATION标签内字符串，正则出kv对
- 考虑使用可视化包graphviz，打算以决策树形式表达树结构，正在将xml文件的树表达方法转换成嵌套字典
- *预计会把显示文档内容和显示文档树结构合并起来，服务器的全局变量可能会有争用问题

#### 20200423
- 字典套列表，在空键情况下需要setdefault(key,[])
- range2NodeID:给了节点的父节点编号，节点的各个子节点值域，重儿子是第几个节点，却没有给子节点编号。于是做了个值域到节点编号的映射，从父亲连儿子。本来如果不考虑重儿子可以直接用编号从儿子连父亲
- ***可能的问题

```
并发下的全局变量、服务器落盘文件
```

- 树结构姑且是显示出来了，目前比较大的妥协：

```
用了决策树可视化方案，决策树的决策路径上的值不能一样，于是并列关系的路径值是1,2,3这样
```

- 误操作的提示待处理


#### 20200424
- 解决掉了图片只能显示一次和自环的bug
- 图片显示一次那个是类的浅拷贝问题
- 在想前端可视化标注怎么实现

#### 20200427
- 可视化标注开发基本完成
- 比较恶心的是前端显示堆叠的问题，设置了absolute的svg对象和设置了absolute的js控件在上方节点有显示变化的时候反应不一致，不设置js控件的absolute的话它又会被svg容器挤压到最下面去，很麻烦
