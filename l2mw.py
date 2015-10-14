#!/usr/bin/env python

#importing l2mw lib
from l2mw import *
from plasTeX.TeX import TeX
import json 

#setting utf8 encoding
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

'''Function that execute a mediawiki_bparser with given parameters'''
def execute_mediawiki_parser(input_path, output_path,\
				title,collapse_level):
	f = open(input_path,'r')
	text = f.read().decode('utf-8')
	###preparser operations
	#reading theorems
	#the preparser result is a tuple of (tex, th_dict)
	preparser_result = preparseTheorems(text)
	#tex object
	tex = TeX()
	tex.input(preparser_result[0])
	tex.ownerDocument.config['files']['filename'] = "." +title+".parsex"
	#parsing DOM
	document = tex.parse()
	#renderer creation\
	rend = MediaWikiRenderer(title)
	#inserting theorem dictionary in renderer
	rend.init_theorems(preparser_result[1])
	#starting rendering
	rend.render(document)
	#after rendering work
	#collapsing pages
	rend.tree.collapseText(collapse_level)
	#fixing refs
	rend.tree.fixReferences()
	#create index
	rend.tree.createIndex(collapse_level)
	#exporting XML
	xml = rend.tree.exportXML()
	#writing to output
	o = open(output_path+".mw",'w')
	o.write(xml)
	o.close()
	#writing debug info
	d = open(output_path+".debug",'w')
	#used_tags
	d.write('USED TAGS:\n')
	for key in sorted(rend.used_tags):
		d.write(key+ ": "+str(rend.used_tags[key])+'\n')
	d.close()
	#exporting tables
	#end.tree.exportFiguresTables()

'''Function that execute a xml_parser with given parameters'''
def execute_xml_parser(input_path, output_path,title):
	f = open(input_path,'r')
	text = f.read().decode('utf-8')
	#the preparser result is a tuple of (tex, th_dict)
	preparser_result = preparseTheorems(text)
	#tex object
	tex = TeX()
	tex.input(preparser_result[0])
	tex.ownerDocument.config['files']['filename'] = output_path+".xml"
	#parsing DOMb
	document = tex.parse()
	#renderer creation
	rend = XMLRenderer()
	#starting rendering
	rend.render(document)


#reading JSON configs
process_data = json.loads(open('configs.txt').read())
for p in process_data:
	input_path = p['input']
	output_path = p['output']
	title = p['title']
	base_path = p['base_path']
	collapse_level= int(p['collapse_level'])
	renderers = p['renderers']
	for r in renderers:
		if r=='mediawiki':
			#base path is added to title (hack)
			if base_path!='':
				title = base_path+ "/"+ title
			execute_mediawiki_parser(input_path,output_path,\
				title,collapse_level)
		elif r =="xml":
			execute_xml_parser(input_path,output_path,title)


