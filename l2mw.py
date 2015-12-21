#!/usr/bin/env python

#importing l2mw lib
from l2mw import *
from plasTeX.TeX import TeX
import json 
import utility

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

	#startin process process
	f = open(input_path,'r')
	#input text must be utf-8 encoded. 
	text = f.read().decode('utf-8')
	###preparser operations
	#reading theorems
	#the preparser result is a tuple of (tex, th_dict)
	pre_export_path= ''
	if(config['print_preparsed_tex']):
		pre_export_path = output_path+".pre"
	preparser_result = preparse_tex(text,pre_export_path)
	#tex object
	tex = TeX()
	tex.input(preparser_result[0])
	#parsing DOM
	document = tex.parse()
	#renderer creation\
	rend_conf = {'doc_title':title,
		'image_extension':config['images_ext'],
		'keywords':config['keywords']}
	rend = MediaWikiRenderer(rend_conf)
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
	if config['create_index']:
		rend.tree.createIndex(collapse_level)
	#exporting 
	export = rend.tree.exportPages(output_path,
					(config['export_format'],
					config['username'], config['userid']) )
	#check if we have to export single pages
	if(config['export_single_pages']):
		#writing single pages
		rend.tree.export_singlePages(config['export_format'],
					output_path+'_pages',(config['username'],
					config['userid']))
	#writing debug info
	d = open(output_path+".debug",'w')
	#used_tags
	d.write('USED TAGS:\n')
	for key in sorted(rend.used_tags):
		d.write(key+ ": "+str(rend.used_tags[key])+'\n')
	d.close()

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
	config['export_format'] = p['export_format']
	config['export_single_pages'] = bool(int(p['export_single_pages']))
	config['create_index'] = bool(int(p['create_index']))
	config['print_preparsed_tex']= bool(int(p['print_preparsed_tex']))
	config['images_ext']= p['images_ext']
	#loading localized keywords
	lang = p['lang']
	config['keywords']= json.loads(open('lang.txt').read())[lang]
	config['username']= p['username']
	config['userid']= p['userid']
	#executing process for alla renderers
	for r in config['renderers']:
		if r=='mediawiki':
			#base path is added to title (hack)
			if config['base_path']!='':
				title = config['base_path']+ "/"+ config['title']
			execute_mediawiki_parser(config)
		elif r =="xml":
			execute_xml_parser(config)


