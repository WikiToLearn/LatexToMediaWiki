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
def execute_mediawiki_parser(config):
	#data
	input_path= config['input_path']
	output_path = config['output_path']
	title = config['title']
	collapse_level = int(config['collapse_level'])

	#process
	f = open(input_path,'r')
	text = f.read().decode('utf-8')
	###preparser operations
	#reading theorems
	#the preparser result is a tuple of (tex, th_dict)
	preparser_export_path= ''
	if(config['print_preparsed_tex']):
		preparser_export_path = output_path+".pre"
	preparser_result = preparse_tex(text,preparser_export_path)
	#tex object
	tex = TeX()
	tex.input(preparser_result[0])
	#tex.ownerDocument.config['files']['filename'] = "." +title+".parsex"
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
	#check if we have to export single pages
	if(config['export_pages']):
		#writing single pages
		rend.tree.exportXML_single_pages(output_path+'_pages')
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
def execute_xml_parser(config):
	#data
	input_path= config['input_path']
	output_path = config['output_path']
	title = config['title']

	#process
	f = open(input_path,'r')
	text = f.read().decode('utf-8')
	#the preparser result is a tuple of (tex, th_dict)
	preparser_export_path= ''
	if(config['print_preparsed_tex']):
		preparser_export_path = output_path+".pre"
	preparser_result = preparse_tex(text,preparser_export_path)
	#tex object
	tex = TeX()
	tex.input(preparser_result[0])
	#parsing DOM
	document = tex.parse()
	#renderer creation
	rend = XMLRenderer()
	#starting rendering
	rend.render(document)


#reading JSON configs
process_data = json.loads(open('configs.txt').read())
config={}
for p in process_data:
	config['input_path'] = p['input']
	config['output_path'] = p['output']
	config['title'] = p['title']
	config['base_path'] = p['base_path']
	config['collapse_level']= int(p['collapse_level'])
	config['renderers'] = p['renderers']
	config['export_pages'] = bool(int(p['export_pages']))
	config['print_preparsed_tex']= bool(int(p['print_preparsed_tex']))
	for r in config['renderers']:
		if r=='mediawiki':
			#base path is added to title (hack)
			if config['base_path']!='':
				title = config['base_path']+ "/"+ config['title']
			execute_mediawiki_parser(config)
		elif r =="xml":
			execute_xml_parser(config)


