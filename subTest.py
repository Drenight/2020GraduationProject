#import os

ans="<p xml soo />\n<p xml soo2 />\n"
fil="chtb_0001.xml"
with open(fil,'r',encoding='utf-8') as f1,open("%s.bak"%fil,'w',encoding='utf-8') as f2:
	flag=0
	for line in f1:
		if(line.strip()=='</RELATION>'):
			flag=0
		if(flag):
			continue
		if(0==flag):
			f2.write(line)
		if(line.strip()=='<RELATION>'):
			flag=1
			f2.write(ans)

	os.remove(file)
	os.rename("%s.bak"%file,file)
		
