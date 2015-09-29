#importing l2mw lib
from l2mw import *
from plasTeX.TeX import TeX

#setting utf8 encoding
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

#XML RENDERER
f = open('tex_sources/DispenseStruttura.tex','r')
text = f.read().decode('utf-8')
tex2 = TeX()
tex2.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'DispenseStruttura.xml'
tex2.input(text)
document2 = tex2.parse()
rend = XMLRenderer()
rend.render(document2)

#MEDIAWIKI RENDERER
f2 = open('tex_sources/DispenseStruttura.tex','r')
text2 = f2.read().decode('utf-8')
tex3 = TeX()
tex3.ownerDocument.config['files']['split-level'] = -100
tex2.ownerDocument.config['files']['filename'] = 'DispenseStruttura.mww'
tex3.input(text2)
document3 = tex3.parse()
rend = MediaWikiRenderer("Test")
rend.render(document3)
#elaborazione
rend.tree.collapseText(0)
rend.tree.fixReferences()
xml = rend.tree.exportXML()
o = open('test.mw','w')
o.write(xml)


#DEBUg PRINTING
#print(str(rend.tree.index))
for k in rend.tree.pages:
	print(str(rend.tree.pages[k]))
	#print(rend.tree.pages[k].text)