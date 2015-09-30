#importing l2mw lib
from l2mw import *
from plasTeX.TeX import TeX

#setting utf8 encoding
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

f = open('tex_sources/test2.tex','r')
text = f.read().decode('utf-8')
#tex object parse the tex
tex2 = TeX()
tex2.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'test.xml'
tex2.input(text)
document2 = tex2.parse()
rend = XMLRenderer()
rend.render(document2)

#MEDIAWIKI RENDERER
f2 = open('tex_sources/test2.tex','r')
text2 = f2.read().decode('utf-8')
#tex object parse the tex
tex3 = TeX()
tex3.ownerDocument.config['files']['split-level'] = -100
tex3.ownerDocument.config['files']['filename'] = 'test.mww'
tex3.input(text2)
document2 = tex3.parse()
#initializing render with Document title
rend2 = MediaWikiRenderer("Prova")
#rendering process start
rend2.render(document2)
##after rendering hooks
#collapsing text to the right page level
rend2.tree.collapseText(1)
#fixing refs
rend2.tree.fixReferences()
#xml exporting
xml = rend2.tree.exportXML('Fisica')
o = open('test.mw','w')
o.write(xml)


#DEBUg PRINTING
#print(str(rend.tree.index))
for k in rend2.tree.pages:
	print(str(rend2.tree.pages[k]))
	#print(rend.tree.pages[k].text)